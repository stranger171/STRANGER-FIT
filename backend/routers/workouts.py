from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database import get_session
from models.workout import Workout
from schemas.workout import WorkoutCreate, WorkoutUpdate
from recommendation.decision_engine import get_recommendation
from recommendation.workout_planner import build_workout_plan
from services.llm_explanation import explain_workout_recommendation
from services.exercise_normalizer import normalize_exercise_name

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)



@router.post("/")
def create_workout(
    workout: WorkoutCreate,
    session: Session = Depends(get_session)
):
    # Step 1: Normalize the exercise name
    normalization = normalize_exercise_name(
        workout.exercise_name
    )

    # Step 2: Reject unrecognized exercise names
    if normalization["status"] in ["invalid", "unrecognized"]:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="Exercise name could not be recognized. Please check the spelling."
        )

    # Step 3: Use the canonical exercise name
    workout_data = workout.model_dump()
    workout_data["exercise_name"] = normalization["canonical_name"]

    # Step 4: Preserve individual set data
    if workout.sets_data is not None:
        workout_data["sets_data"] = [
            workout_set.model_dump()
            for workout_set in workout.sets_data
        ]

    # Step 5: Save the workout
    db_workout = Workout(**workout_data)

    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)

    return {
        "message": "Workout created successfully",
        "workout": db_workout
    }

@router.get("/")
def get_workouts(session: Session = Depends(get_session)):
    workouts = session.exec(select(Workout)).all()

    return {
        "workouts": workouts
    }

@router.get("/progress")
def get_exercise_progress(
    user_id: int,
    exercise_name: str,
    session: Session = Depends(get_session)
):
    from services.exercise_progress import analyze_exercise_progress

    analysis = analyze_exercise_progress(
        user_id=user_id,
        exercise_name=exercise_name,
        session=session
    )

    return {
    "user_id": user_id,
    "exercise_name": exercise_name,
    "sessions": analysis["history"],
    "performance_summary": analysis["performance_summary"],
    "ml_prediction": analysis["ml_prediction"],
    "recommendation": analysis["recommendation"]
}


@router.get("/next-plan")
def get_next_workout_plan(
    user_id: int,
    exercise_name: str,
    session: Session = Depends(get_session)
):
    from services.exercise_progress import analyze_exercise_progress

    analysis = analyze_exercise_progress(
        user_id=user_id,
        exercise_name=exercise_name,
        session=session
    )

    history = analysis["history"]
    recommendation = analysis["recommendation"]
    performance_summary = analysis["performance_summary"]

    if not history:
        return {
            "user_id": user_id,
            "exercise_name": exercise_name,
            "message": "No workout history found",
            "next_workout_plan": None
        }

    if recommendation is None:
        return {
            "user_id": user_id,
            "exercise_name": exercise_name,
            "message": "Not enough workout history to generate a plan",
            "next_workout_plan": None
        }

    latest_sets = history[-1]["sets_data"]

    next_workout_plan = build_workout_plan(
        previous_sets=latest_sets,
        recommendation=recommendation
    )

    explanation = None

    if performance_summary is not None:

        changes = performance_summary["changes"]

        explanation = explain_workout_recommendation(
            progression=analysis["ml_prediction"],
            effort_level=performance_summary["rpe"]["current_effort_level"],
            volume_change_percent=changes["volume_percent"],
            weight_change_kg=changes["heaviest_weight_kg"],
            recommendation=recommendation
        )

    return {
        "user_id": user_id,
        "exercise_name": exercise_name,
        "recommendation": recommendation,
        "next_workout_plan": next_workout_plan,
        "explanation": explanation
    }


@router.get("/latest")
def get_latest_workout(
    user_id: int,
    exercise_name: str,
    session: Session = Depends(get_session)
):
    latest_workout = session.exec(
        select(Workout)
        .where(
            Workout.user_id == user_id,
            Workout.exercise_name == exercise_name
        )
        .order_by(Workout.workout_date.desc())
    ).first()

    if not latest_workout:
        return {
            "message": "No workout found"
        }

    return {
        "workout_id": latest_workout.id,
        "user_id": latest_workout.user_id,
        "workout_date": latest_workout.workout_date,
        "exercise_name": latest_workout.exercise_name,
        "sets_data": latest_workout.sets_data
    }





@router.get("/{user_id}")
def get_user_workouts(
    user_id: int,
    session: Session = Depends(get_session)
):
    workouts = session.exec(
        select(Workout).where(Workout.user_id == user_id)
    ).all()

    return {
        "user_id": user_id,
        "workouts": workouts
    }


@router.get("/{workout_id}/analytics")
def get_workout_analytics(
    workout_id: int,
    session: Session = Depends(get_session)
):
    db_workout = session.get(Workout, workout_id)

    if not db_workout:
        return {
            "message": "Workout not found"
        }

    from services.workout_analytics import analyze_workout_sets

    analytics = analyze_workout_sets(db_workout.sets_data)

    return {
        "workout_id": db_workout.id,
        "exercise_name": db_workout.exercise_name,
        "analytics": analytics
    }


@router.put("/{workout_id}")
def update_workout(
    workout_id: int,
    workout: WorkoutUpdate,
    session: Session = Depends(get_session)
):
    db_workout = session.get(Workout, workout_id)

    if not db_workout:
        return {
            "message": "Workout not found"
        }

    db_workout.workout_date = workout.workout_date
    db_workout.exercise_name = workout.exercise_name
    db_workout.muscle_group = workout.muscle_group
    db_workout.sets = workout.sets
    db_workout.reps = workout.reps
    db_workout.weight_kg = workout.weight_kg
    db_workout.rpe = workout.rpe

    if workout.sets_data is not None:
        db_workout.sets_data = [
            workout_set.model_dump()
            for workout_set in workout.sets_data
        ]

    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)

    return {
        "message": "Workout updated successfully",
        "workout": db_workout
    }


@router.delete("/{workout_id}")
def delete_workout(
    workout_id: int,
    session: Session = Depends(get_session)
):
    db_workout = session.get(Workout, workout_id)

    if not db_workout:
        return {
            "message": "Workout not found"
        }

    session.delete(db_workout)
    session.commit()

    return {
        "message": "Workout deleted successfully"
    }