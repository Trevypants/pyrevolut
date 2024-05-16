# **Contributing Guide**

In order to facilitate a streamlined development process, a few things must be taken into consideration. It is assumed that the reader has already read the [README.md](README.md) file and has a basic understanding of the project structure and the tools used.

## **Setting Up the Development Environment**

To set up the development environment, run the following command in the root directory:

```bash
make setup
```

This will execute the necessary scripts to install all the dependencies and create a virtual environment for the project. To understand what is being run, take a look at the `Makefile` in the root directory. Running `make setup` will run the `.sh` scripts in the `scripts` directory.

If working on MacOs or Linux, make sure to have `curl` capabilities to run the `make setup` command.

## **Pushing Changes**

When pushing changes to the repository, make sure to follow the steps below:

1. Create a new branch with a descriptive name that reflects the changes you are making. For example, if you are adding a new feature, the branch name could be `feature/new-feature`. If you are fixing a bug, the branch name could be `bugfix/fix-bug`.
2. Make the necessary changes in the codebase.
3. Run the tests to ensure that the changes do not break the existing functionality. This can be done by running the following command:

```bash
make test
```

4. If the tests pass, stage the changes to the branch:

```bash
make stage
```

5. Commit the changes with a descriptive message:

```bash
make commit
```

This will bring up an interactive prompt that will guide you through the commit process.

6. Push the changes to the remote repository:

```bash
make push
```

7. Create a pull request on GitHub and assign a reviewer to review the changes.
8. Once the changes have been reviewed and approved, merge the pull request into the `develop` branch.
9. Delete the branch that was created in step 1.
10. Celebrate! 🎉