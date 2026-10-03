#!/usr/bin/env bash
# Load with: source ./env.sh
# Values are exported only into the current shell and its child processes.

# Avoid accidentally echoing secrets if the caller enabled shell tracing.
set +x

read -r -p "Jira URL (e.g. https://example.atlassian.net): " JIRA_URL
read -r -p "Jira account email: " JIRA_USERNAME
read -r -s -p "Jira API token: " JIRA_API_TOKEN
echo
read -r -s -p "GitHub personal access token: " GITHUB_PERSONAL_ACCESS_TOKEN
echo

export JIRA_URL JIRA_USERNAME JIRA_API_TOKEN GITHUB_PERSONAL_ACCESS_TOKEN

read -r -p "Configure Confluence too? [y/N]: " CONFIGURE_CONFLUENCE
if [[ "$CONFIGURE_CONFLUENCE" =~ ^[Yy]$ ]]; then
  read -r -p "Confluence URL (e.g. https://example.atlassian.net/wiki): " CONFLUENCE_URL
  read -r -p "Confluence account email: " CONFLUENCE_USERNAME
  read -r -s -p "Confluence API token (Enter to reuse Jira token): " CONFLUENCE_API_TOKEN
  echo
  if [[ -z "$CONFLUENCE_API_TOKEN" ]]; then
    CONFLUENCE_API_TOKEN="$JIRA_API_TOKEN"
  fi
  export CONFLUENCE_URL CONFLUENCE_USERNAME CONFLUENCE_API_TOKEN
fi

unset CONFIGURE_CONFLUENCE
printf '%s\n' "Credentials are set in this shell. Start Codex from this shell to pass them to MCP servers."
