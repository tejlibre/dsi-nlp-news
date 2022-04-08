# Git feature branches workflow

This article is a quick introduction to using git and using the feature branch workflow

# Git-workflow vs feature branching

When working with Git, there are two prevailing workflows are [Git workflow](https://www.atlassian.com/git/workflows#!workflow-gitflow) and [feature branches](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). IMHO, being more of a subscriber to continuous integration, I feel that the feature branch workflow is better suited, and the focus of this article.

## Setting up a github access token
Since we will be working on github, this step is necessary to have the necessary permissions to pull and push to a github repository. You should [create a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to use in place of a password with the command line or with the API.

## Basic branching

When working in a decentralized workflow, the concepts can be simple. `main` represents the official history and should always deployable. With each new scope of work, aka feature, a developer creates a new branch. For clarity, make sure to use descriptive names like `wip_polarity-gauge-graph` or `wip_LDA-wordcloud-frame` for your branches.

Although you may have a feature like 'emotions`, it may not be appropriate to create a feature branch at this level, there is too much work to be done. It may better to break these large deliverables down to smaller bits of work that can be continuously integrated into the project. Remember, commit early and often. 

That being said, there are times when a single branch will be needed to deliver a large feature or prepare for a release. In this scenario, I'd suggest reading over the [Git Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit) created by the Angular team at Google. As they put it, it is a series of _"... precise rules over how our git commit messages can be formatted"_. 

Before you create a branch, always be sure you have all the upstream changes from the `origin/main` branch. 

### Make sure you are on main

Before I pull, I make sure I am on the right branch. I have GIT Bash autocompletion installed, so this is clear from the prompt. Otherwise, the following command is good to know to list out the branches I have locally as well as designate which branch I am currently on. 

    $ git branch
    
The checked out branch will have a `*` before the name. If the return designates anything other then `main` then switch to main

    $ git checkout main
    
Once on main and ready to pull updates, I use the following:

    $ git pull origin main
    
Depending on your setup, you may even be able to run only the following:

    $ git pull

The `git pull` command combines two other commands, `git fetch` and `git merge`. When doing a `fetch` the resulting commits are stored as a remote branch allowing you to review the changes before merging. Merging, on the other hand, can involve additional steps and flags in the command, but more on that later. For now, I'll stick with `git pull`.

Now that I am all up to date with the remote repo, I'll create a branch. For efficiency, I will use the following:

    $ git checkout -b my-new-feature-branch
    
This command will create a new branch from `main` as well as check out out that new branch at the same time. Doing a `git branch` here again will list out the branches in my local repo and place a `*` before the branch that is checked out.  

      main
    * my-new-feature-branch

### Do you have to be on main to branch from main?

No. There is a command that allows me to create a new branch from any other branch while having checked out yet another branch. WAT?!

    $ git checkout -b transaction-fail-message main
    
In that example, say I was in branch  `github-oauth` and I needed to create a new branch and then check out the new branch? By adding `main` at the end of that command, Git will create a new branch from main and then move me (check out) to that new branch. 

This is a nice command, but make sure you understand what you are doing before you do this. Creating bad branches can cause a real headache when trying to merge back into main. 

## Branch management

When I am working on my new feature branch, it is a good idea to commit often. This allows me to move forward without fear that if something goes wrong, or you have to back out for some reason, I don't lose too much work. Think of committing like that save button habit you have so well programed into you. 

Each commit also tells a little bit about what I just worked on. That's important when other devs on the team are reviewing my code. It's better to have more commits with messages that explain the step versus one large commit that glosses over important details. 

### Commit your code

As I am creating changes in my project, these are all unseated updates. With each commit there most likely will be additions, and there will also be deletions from time to time. To get a baring of the updates I have made, let's get the status.

    $ git status
    
This command will give you a list of all the updated, added and deleted files. 

To add files, I can add them individually or I can add all at once. From the root of the project I can use:

    $ git add .
    
In order to remove deleted files from the version control, I can again either remove individually or from the root address them all like so:

    $ git add -u

I'm lazy, I don't want to think, so I make heavy use of the following command to address all additions and deletions. 

    $ git add --all
    
All the preceding commands will stage the updates for commitment. If I run a `git status` at this point, I will see my updates presented differently, typically under the heading of `Changes to be committed:`. At this point, the changes are only staged and not yet committed to the branch. The next step is to commit with a message. Here is where I lean on the Angular style commit messages linked to above. To commit, do the following:

    $ git commit -m "<type>(<scope>): <subject>"
    
It is considered best to illustrate your comment in the tense that this will do something to the code. It didn't do something in the past and it won't do something in the future. The commit is doing something now. 

A bad subject example would be:

    $ git commit -m "fixed bug with login feature"

A good subject example would be:

    $ git commit -m "fix: update app config to address login bug" 
    
Comments are cheap. For more on how to write expressive commit messages, read [5 Useful Tips For A Better Commit Message](http://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message).


## Push your branch

When working with feature branches on a team, it is typically not appropriate to merge your own code into main. Although this is up to your team as to best manage, the norm is usually to make pull requests. Pull requests require that you push your branch to the remote repo.

To push the new feature branch to the remote repo, simply do the following: 

    $ git push origin my-new-feature-branch

### My branch was rejected?

There is a special case when working on a team and the feature branch being pushed is out of sync with the remote. There are two ways to to address this. A very common approach is to pull.  

    $ git pull origin my-new-feature-branch
    
This will fetch and merge any changes on the remote repo into the local feature branch with all the changes addressing any issues with diffs in the branch's history, now allowing you to push. 

But there is a cost. This merge down will create a broken path in your project's history. A preferred method is to `rebase`. Read below for additional information on this. 

## Working on remote feature branches

When I am creating the feature branch, this is all pretty simple. But when I need to work on a co-workers branch, there are a few additional steps that I follow. 

### Tracking remote branches

My local `.git/` directory will, of course, manage all my local branches, but my local repo is not always aware of any remote branches. To see what knowledge my local branch has of the remote branch index, adding the `-r` flag to `git branch` will return a list.

    $ git branch -r

To keep my local repo 100% in sync with deleted remote branches, I make use of this command:

    $ git fetch -p
    
The `-p` or `--prune` flag, after fetching, will remove any remote-tracking branches which no longer exist. 

### Switching to a new remote feature branch

Doing a `git pull` or `git fetch` will update my local repo's index of remote branches. As long as co-workers have pushed their branch, my local repo will have knowledge of that feature branch. 

By doing a `git branch` you will see a list of your local branches. By doing a `git branch -r` you will see a list of remote branches. 

The process of making a remote branch a local branch to work on is easy, simply check out the branch.

    $ git checkout new-remote-feature-branch
    
This command will pull its knowledge of the remote branch and create a local instance to work on. 

## Keeping current with the main branch

Depending on how long you have been working with your feature branch and how large your dev team is, the `main` branch of your project may be really out of sync from where you created your feature branch. 

When you have completed your update and prior to creating a pull request, you not only have to be up to date in order to merge your new code but also be confident that your code will still work with the latest version of `main`. 

It's here where there are two very different schools of thought. Some teams don't mind if you PULL the latest version from `main`, by simply doing the following. 

    $ git pull origin main
    
This will fetch and merge any changes on the remote repo into the local branch with all the changes, now allowing your feature branch able to be merged. This works for the purpose of merging, but it's kind of gross on the branch's history graph.

Then there are teams who are not a fan of this process, simply because pulling from origin can really screw up the feature branch's history and make it harder to perform more advanced Git features if needed. So, in these situations, it's best to REBASE O_O.

Rebasing a feature branch is not as scary as most make it seem.  All a rebase really is, is taking the updates of the feature branch and moving them to a new spot in the history as to be on top of the latest version of `main`. It's as if you just created that feature branch and made the updates. This creates a very consistent branch history that is easy to follow and easy to work within all situations. 

To rebase your local feature branch off of the latest version of `main`, following these steps will be a guarantee every time. 

```
$ git checkout main         /* ensure you are on the main branch
$ git pull                                   /* pull the latest from the remote 
$ git checkout my-feature-branch      /* checkout the feature branch
$ git push origin my-feature-branch  /* update your copy in the repo
$ git rebase main              /* rebase on the main branch
$ git push origin my-feature-branch --force   /* force update the remote
```

And that's it. This process will ensure that you have the latest version of `main` then take the commits from your feature branch, temporarily unset them, move to the newest head of the `main` branch and then re-commit them. As long as there are no conflicts, there should be no issues. 

### Force push? But ...

Yes, there are those who are not fans of force pushing, but in the case of a feature branch, this is ok. Now force pushing to `main`, well, that's a really bad idea. 

When performing operations like rebasing you are in effect changing the branch's history. When you do this, you can't simply push to the remote as the histories are in conflict, so you will get rejected. To address this, adding the `--force` flag to force push tells the remote to ignore that error and replace the previous history with the new one you just created. 

### Conflicts 

In the worst-case scenario, there is a conflict. This would happen even if you did the pull directly from `main` into the feature branch. To resolve a conflict, read the error report in the command prompt. This will tell you what file has a conflict and where. 

When opening the file you will see a deliberate break in the file's content and two parts that are essentially duplicated, but slightly different. This is the conflict. Pick one of the versions and be sure to delete all the conflict syntax injected into the document. 

Once the conflict(s) is/are resolved, back in the command line you need to add this correction. 

	$ git add .

Once the new updates are staged, you can't commit again as this process is inside a previous commit. So you need to continue with the rebase, like so:

	$ git rebase --continue

If for any reason you get stuck inside a rebase that you simply can't make sense of, you can abort the rebase; 

    $ git rebase --abort

As long as there are no other issues, the rebase will continue and then complete with an output of the updates. 

## The Pull Request

The pull request is where the rubber meets the road. As stated previously, one of the key points of the feature branch workflow is that the developer who wrote the code does not merge the code with `main` until there has been through a peer review. Leveraging Github's pull request features, once you have completed the feature branch and pushed it to the repo, there will be an option to review the diff and create a pull request. 

In essence, a pull request is a notification of the new code in an experience that allows a peer developer to review the individual updates within the context of the update. For example, if the update was on line 18 of `header.html`, then you will only see `header.html` and a few lines before and after line 18. 

This experience also allows the peer reviewer to place a comment on any line within the update that will be communicated back to the editor of origin. This review experience really allows everyone on the team to be actively involved in each update.

Once the reviewer has approved the editor's updates, the next step is to merge the code. While it used to be preferred to merge locally and push main, Git has really grown into this feature and I would argue today it is most preferred to simply use the GUI took in Github.

Now the question is, how to merge? Github has three options; 

1. Create a merge commit
1. Squash and merge
1. Rebase and merge

Creating a merge commit is ok, this will simply merge in the new feature branch code into the `main` branch as long as there are no conflicts. Github will not allow you to merge if it already knows there will be conflicts. 

The squash and merge process is interesting as this will compact all the commits to this feature branch into a single commit to the `main` branch. This may or may not be an issue depending on how your team want's to preserve history. If you are a user of the Angular commits, you may not want to use this feature. 

Lastly, there is the rebase and merge. Showing my preference for rebasing earlier, I am definitely a fan of this merge action. This will do exactly what I explained earlier. It will take all the commits of the feature branch and reset them to the latest head of the `main` branch. If you did a rebase on the feature branch prior to creating a pull request, this process will be seamless and in the end, the most healthy for the project's history.  

### Creating a pull request

The documentations has step by step guide on how to create a pull request in the browser and the command line [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

After initializing a pull request, you'll see a review page that shows a high-level overview of the changes between your branch (the compare branch) and the repository's base branch. You can add a summary of the proposed changes, review the changes made by commits, add labels, milestones, and assignees, and @mention individual contributors or teams. For more information.

Once you've created a pull request, you can push commits from your topic branch to add them to your existing pull request. These commits will appear in chronological order within your pull request and the changes will be visible in the "Files changed" tab.

After you're happy with the proposed changes, you can merge the pull request. If you're working in a shared repository model, you create a pull request and you, or someone else, will merge your changes from your feature branch into the base branch you specify in your pull request. For more information, see [Merging a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)

If status checks are required for a repository, the required status checks must pass before you can merge your branch into the protected branch. For more information, see [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches#require-status-checks-before-merging)

You can link a pull request to an issue to show that a fix is in progress and to automatically close the issue when someone merges the pull request. For more information, see [Linking a pull request to an issue](https://docs.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue)


## Shortcuts using aliases

There are some steps in there that we should just be doing all the time. What about making a single command alias that will cycle through all these commands just so we know things are always in good shape? Yup, we can do that. 

### In Bash

Using Git and Bash is like using a zipper and pants. They just go together. Creating a Bash alias is extremely simple. From your Terminal, enter

    $ open ~/.bash_profile
    
This will open a hidden file in a default text editor. If you have a shortcut command for opening in an editor like Sublime Text or VS Code, use that to open the file. In the file add the following:

    alias refresh="git checkout main && dskil && git pull && git fetch -p"
    
The alias `dskil` is useful for removing annoying `.DS_Store` files. You should have a `.gitignore` file that keeps these out of version control, but I like to keep a clean house too. To make that work, add the following:
    
    alias dskil="find . -name '*.DS_Store' -type f -delete"

With this in your `.bash_profile`, you simply need to enter `refresh` in the command line and POW! 

# References
https://gist.github.com/blackfalcon/8428401
https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/about-collaborative-development-models
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
