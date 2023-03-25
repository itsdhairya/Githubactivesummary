from github import Github
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import smtplib

# Replace this with your personal access token
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN_HERE'

# Create a GitHub object using your access token
g = Github(ACCESS_TOKEN)

# Get your user object
user = g.get_user()

# Get a list of your repositories
repos = user.get_repos()

# Print the names and descriptions of your repositories, as well as their number of stars
repo_names = []
repo_descs = []
repo_stars = []
for repo in repos:
    repo_names.append(repo.name)
    repo_descs.append(repo.description)
    repo_stars.append(repo.stargazers_count)
    print(f"{repo.name} - {repo.description} ({repo.stargazers_count} stars)")

# Generate a word cloud based on the descriptions of your repositories
text = ' '.join(repo_descs)
wordcloud = WordCloud(background_color='white').generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Retrieve the latest commits from your repositories and display their messages and timestamps
commit_messages = []
commit_times = []
for repo in repos:
    commits = repo.get_commits()
    for commit in commits:
        commit_messages.append(commit.commit.message)
        commit_times.append(commit.commit.committer.date)

commit_df = pd.DataFrame({'message': commit_messages, 'time': commit_times})
commit_df.sort_values(by='time', ascending=False, inplace=True)
print("Your latest commits:")
for index, row in commit_df.head().iterrows():
    timestamp = datetime.datetime.strptime(str(row['time']), '%Y-%m-%d %H:%M:%S')
    print(f"{timestamp.strftime('%m/%d/%Y %I:%M %p')} - {row['message']}")

# Send a notification email to your inbox with a summary of your GitHub activity
sender_email = 'YOUR_EMAIL_HERE'
receiver_email = 'YOUR_EMAIL_HERE'
password = 'YOUR_EMAIL_PASSWORD_HERE'

message = f"""Subject: GitHub Activity Summary

Hello,

Here's a summary of your recent GitHub activity:

Repositories:
{text}

Latest Commits:
{commit_df.head().to_string(index=False)}

Thanks for using my program!

Best regards,
Your Python Program
"""
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, password)
    smtp.sendmail(sender_email, receiver_email, message)
