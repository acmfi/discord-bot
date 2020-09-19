from src.extensions.logic.poll.handler import PollHandler


class PollManager:
    def __init__(self):
        self.current_polls = []

    async def add(self, ctx, poll):
        poll_handler = PollHandler(ctx, poll)
        self.current_polls.append(poll_handler)
        await poll_handler.send_poll_n_react(ctx)

    def reaction_should_be_removed(self, reaction):
        poll_handler = list(filter(lambda p: (p.poll.bot_message is not None and
                                              p.poll.bot_message.id == reaction.message.id and
                                              p.poll.is_active) or
                                   p.poll.duration == -1,
                                   self.current_polls))
        if len(poll_handler) == 0:
            return False
        poll_handler = poll_handler[0]
        return reaction.emoji not in poll_handler.poll.get_reaction_emojis()
