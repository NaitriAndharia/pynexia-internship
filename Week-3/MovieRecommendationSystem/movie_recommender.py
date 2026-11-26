import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_sample_dataset() -> pd.DataFrame:
    """Create a clean sample movie dataset for content-based recommendations."""
    movies = [
        {
            "title": "Inception",
            "genre": "Sci-Fi Action Thriller",
            "description": "A thief steals corporate secrets through dream-sharing technology and gets a chance at redemption.",
        },
        {
            "title": "Interstellar",
            "genre": "Sci-Fi Drama Adventure",
            "description": "Explorers travel through a wormhole in space in an attempt to ensure humanity survival.",
        },
        {
            "title": "The Dark Knight",
            "genre": "Action Crime Drama",
            "description": "Batman faces the Joker who brings chaos and moral dilemmas to Gotham City.",
        },
        {
            "title": "The Prestige",
            "genre": "Drama Mystery Thriller",
            "description": "Two rival stage magicians in London compete to create the ultimate illusion.",
        },
        {
            "title": "3 Idiots",
            "genre": "Comedy Drama",
            "description": "Three engineering friends navigate college pressure, friendship, and finding their true passion.",
        },
        {
            "title": "Zindagi Na Milegi Dobara",
            "genre": "Drama Adventure Comedy",
            "description": "Three childhood friends take a road trip across Spain that changes their outlook on life.",
        },
        {
            "title": "Avengers: Endgame",
            "genre": "Action Sci-Fi Adventure",
            "description": "Earth mightiest heroes assemble to reverse catastrophic events and restore balance.",
        },
        {
            "title": "Sherlock Holmes",
            "genre": "Mystery Action Adventure",
            "description": "A sharp detective and his loyal partner solve high-stakes conspiracies in Victorian London.",
        },
        {
            "title": "The Social Network",
            "genre": "Biography Drama",
            "description": "The founding of a massive social networking platform amid legal and personal conflicts.",
        },
        {
            "title": "Gravity",
            "genre": "Sci-Fi Thriller Survival",
            "description": "Two astronauts fight to survive in orbit after debris destroys their spacecraft.",
        },
    ]
    return pd.DataFrame(movies)


class MovieRecommender:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy().reset_index(drop=True)
        self.df["combined_features"] = (
            self.df["genre"] + " " + self.df["genre"] + " " + self.df["description"]
        )
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined_features"])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)

    def recommend_by_movie(self, movie_title: str, top_n: int = 3) -> list[tuple[str, str, float]]:
        matches = self.df[self.df["title"].str.lower() == movie_title.strip().lower()]
        if matches.empty:
            return []

        idx = matches.index[0]
        scores = list(enumerate(self.similarity_matrix[idx]))
        scores = sorted(scores, key=lambda item: item[1], reverse=True)

        recommendations = []
        for movie_idx, score in scores:
            if movie_idx == idx:
                continue
            row = self.df.iloc[movie_idx]
            recommendations.append((row["title"], row["genre"], round(float(score), 3)))
            if len(recommendations) == top_n:
                break
        return recommendations

    def recommend_by_query(self, query: str, top_n: int = 3) -> list[tuple[str, str, float]]:
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        ranked_indices = scores.argsort()[::-1]

        recommendations = []
        for movie_idx in ranked_indices:
            if scores[movie_idx] <= 0:
                continue
            row = self.df.iloc[movie_idx]
            recommendations.append((row["title"], row["genre"], round(float(scores[movie_idx]), 3)))
            if len(recommendations) == top_n:
                break
        return recommendations


def main():
    df = build_sample_dataset()
    recommender = MovieRecommender(df)

    print("=== Movie Recommendation System ===")
    print("Available movies:", ", ".join(df["title"].tolist()))
    print("\n1. Recommend similar movies by title")
    print("2. Recommend movies by genre / mood / keywords")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        title = input("Enter a movie name: ").strip()
        results = recommender.recommend_by_movie(title, top_n=3)
        if not results:
            print(f"Movie '{title}' not found in the dataset.")
        else:
            print(f"\nTop recommendations similar to '{title}':")
            for rank, (rec_title, genre, score) in enumerate(results, start=1):
                print(f"{rank}. {rec_title} ({genre}) — Similarity: {score}")

    elif choice == "2":
        query = input("Enter preferred genre or keywords (e.g., sci-fi space, friendship drama): ").strip()
        results = recommender.recommend_by_query(query, top_n=3)
        if not results:
            print("No matching movies found for your query.")
        else:
            print(f"\nTop recommendations for '{query}':")
            for rank, (rec_title, genre, score) in enumerate(results, start=1):
                print(f"{rank}. {rec_title} ({genre}) — Match Score: {score}")
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()