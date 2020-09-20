from src.extensions.logic.poll.handler import PollHandler


class PollManager:
    """This class will manage all the poll created. 

    The polls are not saved in a db or in the filesystem, so each time the bot restart, the manager will be empty

    Attributes:
        current_polls(PollHandler): List of PollHandler. Each PollHandler is associated with a poll with 
                                    some functions
    """

    def __init__(self):
        """
        Initializes the object
        """
        self.current_polls = []

    async def add(self, poll):
        """
        It will add a new PollHandler to the list. Then the message with the poll will be sent

        Arguments:
            poll(PollModel): Poll that will be added to the handler.
        """
        poll_handler = PollHandler(poll)
        self.current_polls.append(poll_handler)
        await poll_handler.send_poll_n_react()

    def reaction_should_be_removed(self, reaction):
        """
        Checks if a reaction should be removed because the reaction given by the user is not valid.
        This means, that the user used another emoji not given by the bot for the poll. Only will check
        if the poll is active

        Arguments:
            reaction(Reaction): Reaction object (from discord library) and 

        Returns
            boolean: True if the emoji is not one of emojis given in the poll and therefore 
                     the reaction should be removed
        """
        # TODO Add tests for this and maybe should be moved to Handler and create another
        # method here for getting the poll_handler
        poll_handler = list(filter(lambda p: (p.poll.bot_message is not None and
                                              p.poll.bot_message.id == reaction.message.id and
                                              p.poll.is_active) or
                                   p.poll.duration == -1,
                                   self.current_polls))
        if len(poll_handler) == 0:
            return False
        poll_handler = poll_handler[0]
        return reaction.emoji not in poll_handler.poll.get_reaction_emojis()
