#-------------------------------------------------------------------------------
# Name:        Jira Mass Issue Update Script
# Purpose:     Mass updating Jira fields based on user's specified selection.
#              The script can be reused for other fields by changing 'fixVersions'
#              on line 52 to the desired field id.
#
# Author:      Mindaugas Jocius
#
# Created:     11-01-2020
# Copyright:   (c) Mindaugas Jocius 2020
# Licence:     Open Source
#-------------------------------------------------------------------------------

from jira import JIRA

# connect
options = {'server':'https://your_server.atlassian.com'}
jira = JIRA(options, basic_auth=('enter_your_username', 'enter_your_password'))

# enter fixVersion
jiraVersions = []
jiraVersion = input("Enter new fixVersion:")
jiraVersions.append({"name":jiraVersion})
jiraParentIssues = []
jiraParentJQL = input('Enter JQL Query for selecting Jira issues to be updated:') # simply copy the query used in Jira for filtering the issues
jiraSearchforParentIssues = jira.search_issues(jiraParentJQL, maxResults=200)

# extract issue keys
for issue in jiraSearchforParentIssues:
    jiraParentIssues.append(issue.key)

# function for joining issue keys
def jiraListToString(s):
    str1 = ", "
    return (str1.join(s))

# joining issue keys into a single string
jiraParentIssueString = jiraListToString(jiraParentIssues)

# filter query as a string to be used for the selection of Parent issues
jiraSearchforParentQuery = ('parent in (' + jiraParentIssueString + ")")

# selecting Parent issues
jiraSearchforChildIssues = jira.search_issues(jiraSearchforParentQuery)

# selecting Child issues
jiraChildIssues = []
for issue in jiraSearchforChildIssues:
  jiraChildIssues.append(issue.key)
print("Issues to be updated: " + jiraListToString(jiraChildIssues))

# user can validate the list of issues to be updated at this test
startscript = input("Proceed with changes? (y/n)")

# executing the update script
if startscript == "y":
  for issue in jiraSearchforChildIssues: #select issues to be updated
    issue.update(fields={'fixVersions': jiraVersions})
    print(issue.key + ' updated')
  print("Issues updated successfully.")
else:
  print("Program terminated, no issues updated.")