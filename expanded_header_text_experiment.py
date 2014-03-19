"""
Code to take a problem card, and select and add motivational text to
it.  For use in the header text intervention A/B test.
"""

import event_log
import experiments
from intl import i18n
import intl.request
import random
from gae_bingo import identity
import hashlib


explanation_prompt_target_text = {
    "self": i18n._("While you are solving the problem, ask yourself: "),
    "teacher": i18n._("What would you tell your teacher if they asked you "
        "while you were solving the problem: "),
    "sal": i18n._("What would you say if Sal asked you while you were solving "
        "the problem: "),
    "friend": i18n._("While you are solving the problem, how would you answer "
        "another student who asked: "),
}

explanation_prompt_messages = [
    i18n._("What are you doing or thinking right now?"),
    i18n._("Why is what you are currently doing helpful?"),
    i18n._("Why is what you are currently doing useful for achieving your "
        "goal?"),
    i18n._("How well is your current approach to this problem working?"),
    i18n._("For each step, what does this step mean to you?"),
    i18n._("For each step, why is it helpful to take this step?"),
    i18n._("For each step, how do you know this step is right?"),
    ]

# the positive, non growth-mindset, messages
positive_messages = [
    i18n._("Some of these problems are hard. Do your best!"),
    i18n._("This might be a tough problem, but we know you can do it!"),
    i18n._("If at first you don't succeed, try again!"),
    i18n._("The most effective way to do something is to just do it."),
    i18n._("When you get a question wrong, be sure to re-read it carefully."),
    i18n._("When you have a hard time focusing,"
           " take to a moment to clear your head and re-focus."),
    i18n._("Always do your best and you'll get something out of the "
           "experience!"),
    i18n._("Getting enough rest is important to thinking clearly."),
    i18n._("Set your goals high, and don't stop until you get there!"),
    i18n._("We believe in you!"),
    i18n._("Avoiding distractions like television makes learning much "
           "easier."),
    i18n._("Concentrate and you will succeed!"),
    i18n._("The more exercise you get the better you can concentrate!"),
    i18n._("Being organized helps you accomplish more!"),
    ]

# the growth mindset messages
growth_messages = (
    i18n._("Remember, the more you practice the smarter you become!"),
    i18n._("When you learn a new kind of math problem, you grow your math "
           "brain!"),
    i18n._("If this is challenging, you have an opportunity to learn and "
           "become smarter!"),
    i18n._("Mistakes help you learn. Think hard to learn from them."),
    i18n._("The more you learn today, the smarter you'll be tomorrow!"),
    i18n._("The harder you try the better you get!"),
    i18n._("Did you know... Your brain gets better the more you use it."),
    i18n._("If you make a mistake, it's an opportunity to get smarter!"),
    i18n._("Your brain is like a muscle."
           "  The more you flex it, the more powerful it gets!"),
    i18n._("Thinking hard makes your brain grow stronger!"
           "  Think hard about these math exercises."),
    i18n._("Your brain grows new connections every time you practice."
           "  Help your brain grow new connections!"),
    i18n._("When you have to think harder, it makes you smarter!"),
    i18n._("Make your brain more powerful!  Practice hard!"),
    i18n._("Give your brain a workout.  The more you use it,"
           " the stronger it gets."),
    )

# science messages -- these provide a valence neutral control condition
# (and are just fun)
science_messages = (
    i18n._("Did you know: On Mars you would weigh 1/3 as much as on Earth."),
    i18n._("Did you know: An elephant brains weighs 7/2 as much as a human "
           "brain."),
    i18n._("Did you know: If you stare at blue sky you can see white blood "
           "cells moving in your eye."),
    i18n._("Did you know: Sound travels faster in hot air than cold air."),
    i18n._("Did you know: A hurricane has as much energy as thousands of"
    " nuclear bombs."),
    i18n._("Did you know: If you put an empty soda bottle in the freezer,"
    " it will collapse because cold air takes up less space than"
    " hot air."),
    i18n._("Did you know: Red cabbage can detect acids and bases."
    "  Soak red cabbage until the water turns purple."
    "  Try adding lemon or baking soda, and see how the water color changes."),
    i18n._("Did you know: Dolphins can blow rings of bubbles underwater."
    "  Can you?"),
    i18n._("Did you know: Mantis shrimp can detect 12 colors.  Humans can only"
    " detect 3 colors."),
    i18n._("Did you know: Electric fish talk to each other and find mates"
    " using electricity."),
    i18n._("Did you know: Fat has 9/4 as much energy per gram as "
           "carbohydrates or protein."),
    i18n._("Did you know: Your brain uses 1/5 of the energy from the food"
    " you eat."),
    i18n._("Did you know: Cows have four times as many stomachs as you.  You"
    " have one stomach."),
    i18n._("Did you know: Bees tell each other where to find flowers by "
           "wiggling their butts."),
    i18n._("Did you know: Only female mosquitos suck blood."),
    i18n._("Did you know: Goldfish don't have eyelids."),
    i18n._("Did you know: Boy mice sing courtship songs, but they're too"
    " high pitched for us to hear."),
    i18n._("Did you know: Butterflies taste with their hind feet."),
)

whatwhyhow_body = i18n._("""
<p>
    To use this strategy, ask yourself these
    "<span class="hint_purple" style="font-weight: bold">
        What? Why? How?</span>"
    questions while solving a problem.
    <br>
    <span class="hint_purple" style="font-weight: bold">
        What are you doing or thinking right now?</span>
    <br>
    <span class="hint_purple" style="font-weight: bold">
        Why is what you are currently doing helpful?
        Why is it useful for achieving your goal?</span>
    <br>
    <span class="hint_purple" style="font-weight: bold">
        How well is your current approach to this problem
        working?</span>
    <br>
    <br>
    <a href="#" class="show-subhint"
        data-subhint="intervention-whatwhyhow"
        data-hidden-text="Hide Information">
        What if I can't do it?</a>
</p>
<div class="subhint" id="intervention-whatwhyhow">
    Many students are not sure what to say, or think
    their answer isn't good. That is fine, as long as you
    <span style="font-weight: bold; font-style:italic">
        try</span>
    to think about the question, by writing or saying the
    answer to yourself.
</div>
""")


def hash_to_index(max_length, seed, salt=0):
    """
    Generate a pseudorandom integer >= 0 and < max_length, using a hash
    function so it's reproducible.
    """
    # build a hash from the seed and salt
    sig = hashlib.md5(seed + str(salt)).hexdigest()
    # and use the hash to choose an element from the tip string dictionary
    sig_num = int(sig, base=16)
    sig_index = sig_num % max_length
    return sig_index


def hash_to_rand(seed, salt=0):
    """
    Generate a pseudorandom floating point number >= 0 and < 1, using a hash
    function so it's reproducible.
    """
    sig_index = hash_to_index(16 ** 32, seed, salt=salt)
    return float(sig_index) / (16 ** 32)


def random_weighted_choice(alternative_params):
    """
    Return a dictionary key with probability proportional to the value of that
    key.  (does the same thing as ab_test, but draws the condition at random
    each time)
    """
    weighted_choice = lambda s: random.choice(
            sum(([v] * wt for v, wt in s.items()), []))
    return weighted_choice(alternative_params)


def intervention_logging(card, user_exercise):
    """
    Log a bunch of information about the added header text
    """
    event_log.log_event('x.intervention.full_header', card.growthHeader)
    event_log.log_event('x.intervention.exercise_name', card.exercise_name)
    problem_type = getattr(card, 'problem_type', 'UNDEFINED')
    event_log.log_event('x.intervention.problem_type', problem_type)
    total_done = getattr(user_exercise, 'total_done', -1)
    event_log.log_event('x.intervention.total_done', total_done)
    event_log.log_event('x.intervention.language',
            intl.request.locale_for_mo())
    # NOTE - the logging will record events even if the card is never
    # displayed -- for instance, because the student never goes past
    # the first card in a group of cards.  Make sure to compare against
    # problemlog


def add_header_text_to_card(card, user_exercise):
    """
    Adds header text to a problem card based on
    A/B test buckets for the "intervention" set of experiments.
    """

    # use the same ab_test categories for all experiments
    core_categories = ["learning_dashboard", "exercises"]
    # the unique identifier for this user
    bingo_id = identity.identity()

    # get top level A/B test condition
    primary_condition = experiments.CoreMetrics.ab_test(
            "intervention top level",
            alternative_params={
                "no header": 4,
                "intervention": 1,
                "combination": 1},
            core_categories=core_categories)
    event_log.log_event('x.intervention.primary', primary_condition)

    if primary_condition == "no header":
        # student is in control condition
        card.growthHeader = ""
        intervention_logging(card, user_exercise)
        return

    # choose the frequency with which to insert a header
    # above exercises
    frequency_condition = experiments.CoreMetrics.ab_test(
            "intervention frequency",
            alternative_params={
                "0-10": 25,
                "10-25": 25,
                "25-75": 25,
                "75-100": 25},
            core_categories=core_categories)
    # by having continuous frequencies, we can smoothly plot effectiveness
    # vs. frequency later
    if frequency_condition == "0-10":
        frequency = hash_to_rand(bingo_id, 'freq') * 0.1
    elif frequency_condition == "10-25":
        frequency = hash_to_rand(bingo_id, 'freq') * 0.15 + 0.1
    elif frequency_condition == "25-75":
        frequency = hash_to_rand(bingo_id, 'freq') * 0.50 + 0.25
    elif frequency_condition == "75-100":
        frequency = hash_to_rand(bingo_id, 'freq') * 0.25 + 0.75
    event_log.log_event('x.intervention.frequency', frequency_condition)

    if frequency < random.random():
        # no header for this exercise
        card.growthHeader = ""
        event_log.log_event('x.intervention.frequency.skip', 'True')
        intervention_logging(card, user_exercise)
        return

    # choose what kind of psychological intervention to apply
    alternative_params = {
        "repeat experiment": 1,
        "whatwhyhow": 1,
        "individual explanation": 1}
    if primary_condition == "intervention":
        intervention_type_condition = experiments.CoreMetrics.ab_test(
                "intervention type",
                alternative_params=alternative_params,
                core_categories=core_categories)
    elif primary_condition == "combination":
        # in the combination condition, set the subexperiment at
        # random each time
        intervention_type_condition = random_weighted_choice(
                alternative_params)
    event_log.log_event('x.intervention.type', intervention_type_condition)

    if intervention_type_condition == 'repeat experiment':
        # repeat experiment means conditions which are duplicated from the
        # prior growth mindset experiment.
        # This is a nested ab test.
        # the positive statement had a small negative effect in the last
        # experiment, but it's good to have as a control, so we'll only
        # assign a small fraction of students to it this time
        alternative_params = {
            "growth mindset": 10,
            "growth mindset + link": 10,
            "science statement": 10,
            "positive statement": 1,
            }
        if primary_condition == "intervention":
            intervention_repeat_condition = experiments.CoreMetrics.ab_test(
                    "intervention repeat experiment",
                    alternative_params=alternative_params,
                    core_categories=core_categories)
        elif primary_condition == "combination":
            # in the combination condition, set the subexperiment at
            # random each time
            intervention_repeat_condition = random_weighted_choice(
                    alternative_params)
        event_log.log_event('x.intervention.repeat.type',
                intervention_repeat_condition)

        # set the message text for each condition
        if intervention_repeat_condition == "growth mindset":
            message_text = random.choice(growth_messages)
            card.growthHeader = "<p><em>" + message_text + "</em></p>"
        elif intervention_repeat_condition == "growth mindset + link":
            message_text = random.choice(growth_messages)
            message_text = (i18n._('<p><em>%(message)s</em>'
                                 '&nbsp&nbsp&nbsp<FONT SIZE="-5">'
                                 '<a href=/brainworkout_1 target="_blank">'
                                 'LEARN MORE</a>'
                                 '</FONT></p>', message=message_text))
        elif intervention_repeat_condition == "science statement":
            message_text = random.choice(science_messages)
            message_text = "<p><em>" + message_text + "</em></p>"
        elif intervention_repeat_condition == "positive statement":
            message_text = random.choice(positive_messages)
            message_text = "<p><em>" + message_text + "</em></p>"
    elif intervention_type_condition == 'whatwhyhow':
        # nearly identical to the whatwhyhow condition that was run in the
        # metacognitive experiment
        message_text = whatwhyhow_body
    elif intervention_type_condition == 'individual explanation':
        # more light weight explanation effect hints.
        # choose the target of address for the explanation.
        alternative_params = {
            "self": 1,
            "teacher": 1,
            "sal": 1,
            "friend": 1,
            }
        if primary_condition == "intervention":
            target_condition = experiments.CoreMetrics.ab_test(
                    "intervention repeat experiment",
                    alternative_params=alternative_params,
                    core_categories=core_categories)
        elif primary_condition == "combination":
            # in the combination condition, set the subexperiment at
            # random each time
            target_condition = random_weighted_choice(alternative_params)
        target_text = explanation_prompt_target_text[target_condition]
        question_text = random.choice(explanation_prompt_messages)
        message_text = target_text + question_text
        event_log.log_event('x.intervention.explanation.target',
                target_condition)
        event_log.log_event('x.intervention.explanation.question',
                question_text)

    # choose whether there's a dropdown
    dropdown_condition = experiments.CoreMetrics.ab_test(
            "intervention dropdown",
            alternative_params={
                "none": 1,
                "message": 1,
                "specific": 1
                },
            core_categories=core_categories)
    if intervention_type_condition == "whatwhyhow" and (
            dropdown_condition == 'none'):
        # whatwhyhow is a lot of text, and should always appear in a dropdown
        dropdown_condition = 'specific'
    event_log.log_event('x.intervention.dropdown', dropdown_condition)

    # choose the teaser text for the dropdown
    # TODO add bold+color to all dropdown text?
    if dropdown_condition == "message":
        dropdown_text = i18n._("[Click here for a message.]")
    elif dropdown_condition == "specific":
        if intervention_type_condition == 'repeat experiment':
            if intervention_repeat_condition == "science statement":
                dropdown_text = i18n._("[Click to learn a fun science fact.]")
            else:
                dropdown_text = i18n._(
                    "[Click to read a brief motivational message.]")
        elif intervention_type_condition == 'whatwhyhow':
            dropdown_text = i18n._('[Click to learn about the "<span class=' +
                '"hint_purple" style="font-weight: bold">What? Why? How?' +
                '</span>" strategy.]')
        elif intervention_type_condition == 'individual explanation':
            dropdown_text = i18n._("[Click for a learning strategy question.]")

    # combine the dropdown label and the message text
    if dropdown_condition == 'none':
        # just the message text
        card.growthHeader = message_text
    else:
        card.growthHeader = """
            <p>
                <a href="#" class="show-subhint"
                   data-subhint="intervention-learn-more"
                   data-hidden-text="Hide Information">
                    %s
                </a>
            </p>
            <div class="subhint" id="intervention-learn-more">
                %s
            </div>""" % (dropdown_text, message_text)

    intervention_logging(card, user_exercise)
