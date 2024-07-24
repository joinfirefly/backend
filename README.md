# Graphene BE
Graphene's Backend Server

Powered by [FastAPI](https://fastapi.tiangolo.com) with [Prisma](https://prisma.io) ([prisma-client-py](https://github.com/RobertCraigie/prisma-client-py))

## Getting Started
> [!WARNING]
> Graphene-BE is under development. Therefore, its use in a production environment is deprecated.
By following this guide, you can build an instance of Graphene.

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Inspired
Most of Graphene's functionality (except for the back-end plugin system, etc.) is based on Misskey.

Graphene is inspired by the following software:
  * Misskey (reactions, Graphen FE's plugin system, etc)
  * Pleroma (Replaceable frontend)

## Todo
- [ ] Backend
  - [ ] ActivityPub (1/8 done)
    - [x] webfinger
    - [ ] Person
    - [ ] Instance Actor
    - [ ] Inbox
    - [ ] Outbox
    - [ ] Post Activity To Remote
      - [ ] Convert MFM to HTML
    - [ ] Parse Activity
    - [ ] HTTP Signatures
  - [ ] API ( 0/? done)
  - [ ] User
    - [ ] Create Account
    - [ ] Create Note
    - [ ] Create Reaction
  - [ ] CloudFlare Turnstile
  - [ ] email verification
    - [ ] can opt-out of email verification
  - [ ] Media can be stored in S3 and S3 compatible storage
  - [ ] Misskey's summaly proxy support
  - [ ] Allow registration to be approved/or invite code-based (from Misskey (and Sharkey))
- [ ] Frontend
  - [x] login
  - [x] signup
    - [x] CloudFlare Turnstile
  - [ ] password reset
    - [x] CloudFlare Turnstile
  - [ ] Profile
  - [ ] Note
    - [ ] Render MFM
    - [ ] Reaction
    - [ ] Reply
    - [ ] Show Replies/Quote
  - [ ] Rewrite With Vue3