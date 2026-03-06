#!/usr/bin/env python3
"""
Create AWS Amplify app linked to GitHub repository with auto-deploy
"""

import boto3
import json

# Configuration
REGION = 'us-east-2'
REPO_OWNER = 'rventra'
REPO_NAME = 'stock-analysis-dashboard'
REPO_BRANCH = 'master'
APP_NAME = 'stock-analysis-dashboard'
DESCRIPTION = 'AI-powered stock analysis dashboard'

def create_amplify_app():
    """Create Amplify app and link to GitHub"""

    # Initialize Amplify client
    amplify = boto3.client('amplify', region_name=REGION)

    # First, create the Amplify app
    print(f"[1/3] Creating Amplify app: {APP_NAME}")

    try:
        response = amplify.create_app(
            name=APP_NAME,
            description=DESCRIPTION,
            platform='WEB',
            enableAutoBranchCreation=True,
            autoBranchCreationPatterns=['*'],
            enableBranchAutoDeletion=True,
            enableBranchAutoBuild=True
        )
        app_id = response['app']['appId']
        print(f"  Created app with ID: {app_id}")
    except Exception as e:
        if 'App already exists' in str(e):
            # Get existing app
            print("  App already exists, fetching...")
            apps = amplify.list_apps(max_results=10)
            for app in apps['apps']:
                if app['name'] == APP_NAME:
                    app_id = app['appId']
                    print(f"  Using existing app: {app_id}")
                    break
        else:
            raise e

    # Wait for app to be ready
    print(f"\n[2/3] Waiting for app to be ready...")
    import time
    for i in range(10):
        try:
            status = amplify.get_app(appId=app_id)['app']['status']
            print(f"  Status: {status}")
            if status == 'ACTIVE':
                break
        except Exception as e:
            print(f"  Error: {e}")
        time.sleep(2)

    # Create branch
    print(f"\n[3/3] Creating branch '{REPO_BRANCH}'...")

    try:
        # Create the branch
        amplify.create_branch(
            appId=app_id,
            branchName=REPO_BRANCH,
            enableAutoBuild=True,
            framework='Static'
        )
        print(f"  Created branch: {REPO_BRANCH}")
    except Exception as e:
        if 'Branch already exists' in str(e):
            print(f"  Branch '{REPO_BRANCH}' already exists")
        else:
            print(f"  Note: {e}")

    print(f"\n{'='*60}")
    print(f"SUCCESS! Amplify App Created")
    print(f"{'='*60}")
    print(f"App ID: {app_id}")
    print(f"App Name: {APP_NAME}")
    print(f"Console URL: https://console.aws.amazon.com/amplify/apps/{app_id}/")
    print(f"\nNext steps:")
    print(f"1. Open the Console URL above")
    print(f"2. Connect your GitHub repository")
    print(f"3. Select {REPO_OWNER}/{REPO_NAME}")
    print(f"4. Select branch: {REPO_BRANCH}")
    print(f"5. Build settings: 'No build' (static site)")
    print(f"6. Deploy!")

    return app_id

if __name__ == "__main__":
    create_amplify_app()
