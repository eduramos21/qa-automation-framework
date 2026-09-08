# Conventions for my-stack

This file is the style guide the author and maintainer agents follow when they
write code in this stack. `profile.yaml` says where files go and how to run
them. This file says what good looks like once you are inside a file.

Write it the way you would brief a new engineer on their first day. Show code,
not adjectives. Every rule below should have an example that can be copied.

## Test file shape

Show one complete, real test. Not pseudocode. The agent pattern matches on it.

## Naming

How test files, test titles, page objects and fixtures are named.

## Locators

Which strategies to use and in what order, and which ones are banned here.
`profile.yaml` has the ordered list, this is where you explain the edge cases.

## Waiting

How this stack waits for things. Name the API that replaces a fixed sleep.

## Page objects

When one earns its existence, what belongs in it, what does not. The common
failure is a page object per page whether or not it holds anything, so say
where the line is.

## Fixtures and setup

How a test gets a logged in session, a seeded record, a clean database. Include
teardown.

## Assertions

The assertion API, and how to write a failure message that says what went wrong
without opening the file.

## Test data

Where it comes from, how it is isolated between parallel workers.

## What not to do

The specific mistakes people make in this stack. This section is the one the
agents lean on most, so be blunt and be specific.
