import sys
import urllib.request
import urllib.error
import json

# Mapping of GitHub event types to human-readable descriptions
EVENT_MAP = {
    "CommitCommentEvent": "Commented on a commit in",
    "CreateEvent": "Created a branch, tag, or repository in",
    "DeleteEvent": "Deleted a branch or tag in",
    "DiscussionEvent": "Participated in a discussion in",
    "ForkEvent": "Forked",
    "GollumEvent": "Updated the wiki in",
    "IssueCommentEvent": "Commented on an issue in",
    "IssuesEvent": "Created, edited, or closed an issue in",
    "MemberEvent": "Added or removed a collaborator in",
    "PublicEvent": "Made public the repository",
    "PullRequestEvent": "Opened, merged, or closed a pull request in",
    "PullRequestReviewEvent": "Reviewed a pull request in",
    "PullRequestReviewCommentEvent": "Commented on a pull request review in",
    "PushEvent": "Pushed commits to",
    "ReleaseEvent": "Published a release in",
    "WatchEvent": "Starred",
}


def get_events(username):
    """Fetch and display recent GitHub activity for a given username."""
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status != 200:
                print(f"Error fetching data. HTTP {response.status}")
                return

            data = response.read()
            events = json.loads(data)

            if not events:
                print("No recent activity found.")
                return

            for event in events:
                event_type = event.get('type', 'N/A')
                action = EVENT_MAP.get(event_type, event_type)
                repo_name = event.get('repo', {}).get('name', 'N/A')
                created_at = event.get('created_at', 'N/A')
                if len(created_at) > 3:
                    created_at = created_at[:10]
                print(f"{action} {repo_name} at {created_at}")
    except urllib.error.HTTPError as e:
        print(f"Error fetching data: {e}")


def main():
    """Command-line interface handler."""
    args = sys.argv[1:]

    if not args:
        print("Usage: github-activity-cli [username]")
        return

    username = args[0]

    if username:
        get_events(username)


if __name__ == "__main__":
    main()
