"""
abtest_learningstrategies.py contains the latest AB Test to encourage learning strategies. 
CMD + F for STOPSHIP to move through explanations of each key change.

SUMMARY EXPLANATION for current version:
The new experiment starts with the "KIND OF HEADER" A/B test, where
    "no header" as before does not affect users
    "header" means a header text message is added that does NOT have links to more info, like mindset/explanation prompts.
    "learning support" has 2 subconditions. 
        In each subcondition it adds a header with a clickable link that reveals
a sequence of prompts and messages that a user can choose
to expand by clicking on links that reveal DropDown or Mouseover text
See tiny.cc/kalearningcoach for a demo.
    "learning support.dropdown link" subcondition reveals text on dropdown that provides the
LearningCoach study information via a nested series of clickable links.See tiny.cc/kalearningcoach
    "learning support.webpage link" subcondition provides a link to a webpage on KA 
with basically just the LearningCoach study information (like brain workout page in mindset study).
Although right now there's just a placeholder, the same tiny.cc/kalearningcoach.
    The advantage of adding this webpage with equivalent information is that we can then measure
who actually clicked on it, as we're doing for the brain_workout page
(which Jascha said would be challenging for the "dropdown link" 
version. Also, this could test the willingness of students to use external study resources.
And it could make any later A/B testing of different versions of the LearningCoach easier,
because then A/B testing can take place *only* on the target webpage, instead of in exercises.


Older notes:
The code takes a list of problem cards, and select and add text to 
each of the problem cards. 
"""

import experiments
import random
import event_log

# the names of the exercises being targeted with this intervention.
# Currently same as the Growth Mindset experiment.
target_exercises = [
    'adding_and_subtracting_fractions',
    'adding_fractions',
    'adding_fractions_with_common_denominators',
    'changing_fractions_to_decimals_1',
    'changing_fractions_to_percents',
    'changing_percents_to_fractions',
    'comparing_fractions_1',
    'comparing_fractions_2',
    'comparing_improper_fractions_and_mixed_numbers',
    'converting_decimals_to_fractions_1',
    'converting_decimals_to_fractions_2',
    'converting_fractions_to_decimals',
    'converting_mixed_numbers_and_improper_fractions',
    'converting_repeating_decimals_to_fractions_1',
    'converting_repeating_decimals_to_fractions_2',
    'dividing_fractions',
    'dividing_fractions_0.5',
    'dividing_fractions_alternative',
    'dividing_fractions_word_problems',
    'equivalent_fractions',
    'equivalent_fractions_2',
    'expressing_ratios_as_fractions',
    'fractions_cut_and_copy_1',
    'fractions_cut_and_copy_2',
    'fractions_on_the_number_line_1',
    'fractions_on_the_number_line_2',
    'fractions_on_the_number_line_3',
    'fraction_word_problems_1',
    'multiplying_fractions',
    'multiplying_fractions_0.5',
    'multiplying_fractions_word_problems',
    'ordering_fractions',
    'ordering_improper_fractions_and_mixed_numbers',
    'recognizing_fractions',
    'recognizing_fractions_0.5',
    'simplifying_fractions',
    'subtracting_fractions',
    'subtracting_fractions_with_common_denominators',
    ]

# the growth mindset messages
growth_messages = [
    "Remember, the more you practice the smarter you become!",
    "When you learn a new kind of math problem, you grow your math brain!",
    "If this is challenging, you have an opportunity to learn and become"
    " smarter!",
    "Mistakes help you learn. Think hard to learn from them",
    "The more you learn today, the smarter you'll be tomorrow!",
    "The harder you try the better you get!",
    "Did you know... Your brain gets better the more you use it.",
    "If you make a mistake, it's an opportunity to get smarter!",
    "Your brain is like a muscle."
    "  The more you flex it, the more powerful it gets!",
    "Thinking hard makes your brain grow stronger!"
    "  Think hard about these math exercises.",
    "Your brain grows new connections every time you practice."
    "  Help your brain grow new connections!",
    "When you have to think harder, it makes you smarter!",
    "Make your brain more powerful!  Practice hard!",
    "Give your brain a workout.  The more you use it,"
    " the stronger it gets.",
    ]


#the what why how study strategy
wwh_strat = ('<a href="#" class="show-subhint" data-subhint="what-why-how">'
                              'Click here to learn about the'
                              ' "<span class="hint_purple" style="font-weight:bold">What? Why? How?</span> strategy</a>'
                              '<div class="subhint" id="what-why-how">'
                              'To use this strategy, ask yourself these'
                              ' "<span class="hint_purple" style="font-weight: bold">'
                              'What? Why? How?</span>"'
                              ' questions after each hint in a problem.'
                              '<br><span class="hint_purple" style="font-weight: bold">'
                              'What does this step mean to you?</span>'
                              '<br>'
                              '<span class="hint_purple" style="font-weight: bold">'
                              'Why is it helpful to take this step?</span>'
                              '<br><span class="hint_purple" style="font-weight: bold">'
                              'How do you know this step is right?</span>'
                              '<br>'
                              '<br><br>'
                              '<a href="#" class="show-subhint" data-subhint="encouragement" data-hidden-text="Hide Information">'
                              'What if I can’t do it?</a>'
                              '<div class="subhint" id="encouragement">'
                              'Many students are not sure what to say, or think '
                              'their answer isn’t good. That is fine, as long as you'
                              '<span style="font-weight: bold; font-style:italic">'
                              ' try</span>'
                              ' to think about the question, by typing or saying the answer to yourself.'
                              '</div></div>')








def add_header_text_to_cards(card, user_exercise):
    """
   Adds header text to a problem card based on exercise and
   A/B test bucket.
   """

    if not (card.exercise_name in target_exercises):
        card.growthHeader = ""     # card refers to the problem object. growthHeader is an attribute of the card.
        return

    # STOPSHIP. The new experiment starts with the KIND OF HEADER A/B test. 
    test_condition = experiments.CoreMetrics.ab_test("KIND OF HEADER",
            alternative_params={
                "no header": 5, # STOPSHIP. As before, unaffected users.
                "header": 1, # Text message is added but NO links to more info. 
                "learning support": 1, # Header has a clickable link to DropDown text or a webpage.
                },
            core_categories='all')

    if test_condition == "no header":
        card.growthHeader = ""
        
    elif test_condition == "header":
        test_subcondition = experiments.CoreMetrics.ab_test(
            "learning support subtest",
            alternative_params={
                "mindset only": 1, # mindset message, exactly as in previous expt            
                "explanation only": 1, #provides dropdown explanation strategy
                "mindset + explanation": 1}, #provides a combination
            core_categories='all')
        test_condition += "." + test_subcondition
        message = random.choice(mindset_messages)
        card.growthHeader = "<p><em>" + message + "</em></p>"
        
    elif test_condition == "learning support":
        # STOPSHIP. People in the "learning support" condition are assigned to 1 of 2 sub-conditions.
        # "webpage link" provides a link to a webpage on KA with the LearningCoach study information (like brain workout page in mindset study).
        # Right now this is just a placeholder exercise on our server with the LearningCoach at top.
        # "dropdown link" reveals text on dropdown that provides the LearningCoach study information
        # through a nested series of dropdown text.

        test_subcondition = experiments.CoreMetrics.ab_test(
            "learning support subtest",
            alternative_params={
                "webpage link": 1, # provides a link to a webpage on KA with the LearningCoach study information               
                "dropdown link": 1}, # reveals text on dropdown that provides the LearningCoach study information
            core_categories='all')
        test_condition += "." + test_subcondition
        


    # STOPSHIP. "webpage link" provides a link to a webpage on KA with the LearningCoach study information (like brain workout page in mindset study).
    # Right now this is just a placeholder exercise on our server with the LearningCoach at top.
        if test_condition == "learning support.webpage link":
            card.growthHeader = ('<p><em>Click here to get tips for motivating yourself and learning more quickly:</em>'
                             '&nbsp&nbsp&nbsp<FONT SIZE="-5">'
                             '<a href="http://tiny.cc/kalearningcoach" target="_blank">' # This is a placeholder link to rough demo, actual link can be on KA like brain workout.
                             'GET TIPS</a>'
                             '</FONT></p>')
    # STOPSHIP. "dropdown link" reveals text on dropdown that provides the LearningCoach study information
    # through a nested series of dropdown text.                             
    # You can easily see what this complicated code does through demo at tiny.cc/kalearningcoach       
        elif test_condition == "learning support.dropdown link":
            message = random.choice(growth_messages) # These are assigned here and then used INSIDE of the LearningCoach
            card.growthHeader = ('<p><a href="#" class="show-subhint" data-subhint="help-me">'
                              'Click here to get tips for motivating yourself and learning more quickly</a></p>'
                              '<div class="subhint" id="help-me">'
                              '<a href="#" class="show-subhint" data-subhint="mindset-message">'
                              'I&#39;m feeling discouraged, I&#39;d like a motivational message.</a>'
                              '<div class="subhint" id="mindset-message"><p>' + message + '</p>'
                              '<p><a href="#" class="show-subhint" data-subhint="mindset-tellmore">Tell me more!</a></p>'
                              '<div class="subhint" id="mindset-tellmore">'
                              'Even if it&#39;s tough, the time you spend working help you form more '
                              'connections that will help you solve future problems.</div>'
                              '<p><a href="#" class="show-subhint" data-subhint="mindset-altmore">'
                              'How do you motivate yourself?</a></p>'                            
                              '<div class="subhint" id="mindset-altmore">'
                              'What would you tell another student to get motivated?</div>'
                              '</div>'
                              '<p><a href="#" class="show-subhint" data-subhint="learn-strat">'
                              'Would you like some suggestions for problem-solving strategies?</a></p>'
                              '<div class="subhint" id="learn-strat">'+ wwh_strat + '</div></div>')
                              


    



        
    # TODO - this will record events even if the card is never
    # displayed -- for instance, because the student never goes past
    # the first card in a group of cards.  When interpreting these
    # results, will need to do the extra work of matching these up
    # against problemlog entries, and throwing out the ones which
    # don't match.
    event_log.log_event('x.mindset.test_condition', test_condition)
    event_log.log_event('x.mindset.exercise_name', card.exercise_name)
    problem_type = getattr(card, 'problem_type', 'UNDEFINED')
    event_log.log_event('x.mindset.problem_type', problem_type)
    total_done = getattr(user_exercise, 'total_done', -1)
    event_log.log_event('x.mindset.total_done', total_done)
    event_log.log_event('x.mindset.message_text', card.growthHeader)
