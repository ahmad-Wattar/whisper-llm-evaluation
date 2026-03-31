import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


def main():
    # --- 1️⃣ DataFrame laden ---
    df = pd.read_parquet("clean_llm_experiments_with_embeddings.parquet")

    # --- 2️⃣ Modell laden ---
    model = SentenceTransformer(
        "aari1995/German_Semantic_V3b",
        trust_remote_code=True,
        device="cpu"  # bei cuda hat es nicht geklappt: CUDA out of memory
    )

    # --- 3️⃣ Neue Spalte definieren ---
    col_name = "aari1995/German_Semantic_V3b"
    df[col_name] = None

    # --- 4️⃣ Embeddings berechnen ---
    texts = df["text"].fillna("").tolist()
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        #batch_size=1,          # effizienter auf GPU ich brauche das nicht auf cpu
        normalize_embeddings=True
    )

    # --- 5️⃣ Embeddings in DataFrame speichern ---
    df[col_name] = embeddings.tolist()

    # --- 6️⃣ Wieder speichern ---
    df.to_parquet("last_clean_llm_experiments_with_embeddings.parquet")

    print(f"✅ {len(df)} Embeddings mit aari1995/German_Semantic_V3b berechnet und in '{col_name}' gespeichert.")


if __name__ == "__main__":
    main()
