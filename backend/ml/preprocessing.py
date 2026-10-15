from sklearn.preprocessing import OneHotEncoder


def encode_effort_level(effort_level: str) -> list[int]:
    encoder = OneHotEncoder(
        categories=[["Low", "Moderate", "High"]],
        sparse_output=False
    )

    encoded = encoder.fit_transform([[effort_level]])

    return encoded[0].astype(int).tolist()