import pandas as pd
import os

INPUT_FILE = "data/twcs.csv"
OUTPUT_FILE = "data/applesupport_conversations.csv"

BRAND = "AppleSupport"


def load_data():
    df = pd.read_csv(INPUT_FILE, encoding="latin-1")

    required_columns = [
        "tweet_id",
        "author_id",
        "inbound",
        "created_at",
        "text",
        "response_tweet_id",
        "in_response_to_tweet_id"
    ]

    df = df[required_columns]
    return df


def extract_brand_conversations(df):
    # Get tweets written by AppleSupport
    support = df[df["author_id"] == BRAND].copy()

    # Keep AppleSupport tweets that are replies
    support = support[
        support["in_response_to_tweet_id"].notna()
    ].copy()

    # Convert parent tweet IDs to integers
    support["parent_id"] = (
        support["in_response_to_tweet_id"]
        .astype(int)
    )

    # Get customer tweets
    customers = df[df["inbound"] == True].copy()

    # Rename columns before merging
    customers = customers.rename(
        columns={
            "tweet_id": "customer_tweet_id",
            "author_id": "customer_id",
            "text": "customer_message",
            "created_at": "customer_created_at"
        }
    )

    # Connect customer tweet to AppleSupport reply
    conversations = support.merge(
        customers[
            [
                "customer_tweet_id",
                "customer_id",
                "customer_message",
                "customer_created_at"
            ]
        ],
        left_on="parent_id",
        right_on="customer_tweet_id",
        how="inner"
    )

    conversations = conversations.rename(
        columns={
            "tweet_id": "support_tweet_id",
            "text": "support_reply",
            "created_at": "support_created_at"
        }
    )

    # Keep only useful columns
    conversations = conversations[
        [
            "customer_tweet_id",
            "customer_id",
            "customer_message",
            "customer_created_at",
            "support_tweet_id",
            "support_reply",
            "support_created_at"
        ]
    ]

    return conversations


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)
    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")
    text = text.replace("&amp;", "&")

    return " ".join(text.split())


def main():
    print("Loading dataset...")
    df = load_data()

    print("Total tweets:", len(df))

    print("Extracting AppleSupport conversations...")
    conversations = extract_brand_conversations(df)

    # Clean messages
    conversations["customer_message"] = (
        conversations["customer_message"]
        .apply(clean_text)
    )

    conversations["support_reply"] = (
        conversations["support_reply"]
        .apply(clean_text)
    )

    # Remove empty messages
    conversations = conversations[
        conversations["customer_message"].str.len() > 0
    ]

    os.makedirs("data", exist_ok=True)

    conversations.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("\nDone!")
    print("AppleSupport conversations:", len(conversations))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
