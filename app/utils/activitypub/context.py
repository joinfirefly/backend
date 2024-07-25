async def check_available_context(actor: dict):
    if "https://www.w3.org/ns/activitystreams" not in actor["@context"]:
        raise
    c = []
    for context in actor["@context"]:
        if isinstance(context, dict):
            for k in context.keys():
                if k == "toot":
                    if context[k] == "http://joinmastodon.org/ns#":
                        c["toot"] = []
                elif k == "schema":
                    if context[k] == "http://schema.org#":
                        c["schema"] = []
                elif k == "misskey":
                    if context[k] == "https://misskey-hub.net/ns#":
                        c["misskey"] = []
                if context[k].startswith("toot:"):
                    if not c.get("toot"):
                        pass
                    else:
                        c["toot"].append(context[k][5:])
                elif context[k].startswith("schema:"):
                    if not c.get("schema"):
                        pass
                    else:
                        c["schema"].append(context[k][7:])
                elif context[k].startswith("misskey:"):
                    if not c.get("misskey"):
                        pass
                    else:
                        c["misskey"].append(context[k][7:])
                else:
                    c.