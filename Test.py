from sqlalchemy import text
from db.query import changePost, deletePost, getFeed, get_session  # replace 'your_module' with your filename

def setup_test_data():
    session = get_session()
    try:
        # Create test user
        session.execute("INSERT INTO USER (UserID, Username) VALUES (:id, :name)", {"id": 999, "name": "TestUser"})
        # Create test post
        session.execute("INSERT INTO POST (PostID, Title, Content, Date) VALUES (:id, :title, :content, NOW())",
                        {"id": 999, "title": "Test Post", "content": "Original content"})
        # Link user to post in CREATES table
        session.execute("INSERT INTO CREATES (UserID, PostID) VALUES (:uid, :pid)", {"uid": 999, "pid": 999})
        session.commit()
        print("Test data setup complete.")
    except Exception as e:
        session.rollback()
        print("Error setting up test data:", e)
    finally:
        session.close()

def cleanup_test_data():
    session = get_session()
    try:
        session.execute("DELETE FROM COMMENT WHERE POSTID = 999")
        session.execute("DELETE FROM CREATES WHERE POSTID = 999")
        session.execute("DELETE FROM POST WHERE POSTID = 999")
        session.execute("DELETE FROM USER WHERE UserID = 999")
        session.commit()
        print("Test data cleaned up.")
    except Exception as e:
        session.rollback()
        print("Error cleaning up test data:", e)
    finally:
        session.close()

def test_functions():
    test_userid = 999
    test_postid = 999
    new_content = "Updated content for testing."

    print("===== TEST: changePost =====")
    if changePost(test_userid, test_postid, new_content):
        print("Post updated successfully.")
    else:
        print("Failed to update post.")

    print("\n===== TEST: getFeed =====")
    feed = getFeed(test_userid)
    if feed:
        print("Feed retrieved:")
        for post in feed:
            print(f"Title: {post[0]}, Date: {post[1]}, Content: {post[2]}")
    else:
        print("No feed found.")

    print("\n===== TEST: deletePost =====")
    if deletePost(test_userid, test_postid):
        print("Post deleted successfully.")
    else:
        print("Failed to delete post.")

    # Verify deletion
    session = get_session()
    try:
        result = session.execute(text("SELECT * FROM POST WHERE POSTID = :id"), {"id": test_postid}).fetchall()
        if not result:
            print("Post deletion confirmed.")
        else:
            print("Post still exists:", result)
    finally:
        session.close()

if __name__ == "__main__":
    setup_test_data()
    test_functions()
    cleanup_test_data()
