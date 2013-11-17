def add_header_text_to_cards(card, user_exercise):
    """
   Adds header text to a problem card based on exercise and
   A/B test bucket.
   """

    if not (card.exercise_name in target_exercises):
        card.growthHeader = ""     # card refers to the problem object. growthHeader is an attribute of the card.
        return

    # A/B test condition. “KIND OF HEADER”
    # learning support is the coach or mindset + link, header (for now) just corresponds to "growth mindset" from old expt
    test_condition = experiments.CoreMetrics.ab_test("learning support and header",
            alternative_params={
                "no header": 5,
                "learning support": 1, 
                "header": 1},
            core_categories='all')

    if test_condition == "learning support":
        # nested experiments because only 4 conditions are supported in
        # GAE/Bingo
        
        # Single Scaffold is the learning coach, message + link is just the growth mindset+ link for original expt.
       
        test_subcondition = experiments.CoreMetrics.ab_test(
            "learning support subtest",
            alternative_params={
                "single scaffold": 1,                
                "message + link": 1},
            core_categories='all')
        test_condition += "." + test_subcondition
        
    if test_condition == "no header":
        card.growthHeader = ""
        
    elif test_condition == "learning support.message + link":
        message = “Click here to get tips for motivating yourself and learning more quickly:”
        card.growthHeader = ('<p><em>' + message + '</em>'
                             '&nbsp&nbsp&nbsp<FONT SIZE="-5">'
                             '<a href=/brainworkout_1 target="_blank">'
                             'LEARN MORE</a>'
                             '</FONT></p>')
                             
    elif test_condition == "learning support.single scaffold":

        card.growthHeader = ('<p><a href="#" class="show-subhint" data-subhint="help-me">Click here for learning tips</a></p>'
                              '<div class="subhint" id="help-me">'
                              '<a href="#" class="show-subhint" data-subhint="mindset-message">I&#39;m feeling discouraged, I&#39;d like a motivational message.</a>'
                              '<div class="subhint" id="mindset-message"><p>' + message + '</p>'
                              '<p><a href="#" class="show-subhint" data-subhint="mindset-tellmore">Tell me more!</a></p>'
                              '<div class="subhint" id="mindset-tellmore">'
                              'Even if it&#39;s tough, the time you spend working help you form more connections that will help you solve future problems.</div>'
                              '<p><a href="#" class="show-subhint" data-subhint="mindset-altmore">How do you motivate yourself?</a></p>'                            
                              '<div class="subhint" id="mindset-altmore">What would you tell another student to get motivated?</div>'
                              '</div>'
                              '<p><a href="#" class="show-subhint" data-subhint="learn-strat">Would you like some suggestions for problem-solving strategies?</a></p>'
                              '<div class="subhint" id="learn-strat">'
                              '<a href="#" class="show-subhint" data-subhint="what-why-how">Click here to learn about the'
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
                              'As a reminder to ask yourself these questions, they'
                              'will sometimes appear in '
                              '<span class="hint_purple" style="font-weight: bold">'
                              'purple</span>.'
                              '<br><br>'
                              '<a href="#" class="show-subhint" data-subhint="encouragement" data-hidden-text="Hide Information">'
                              'What if I can’t do it?</a>'
                              '<div class="subhint" id="encouragement">'
                              'Many students are not sure what to say, or think '
                              'their answer isn’t good. That is fine, as long as you'
                              '<span style="font-weight: bold; font-style:italic">'
                              ' try</span>'
                              ' to think about the question, by typing or saying the answer to yourself.'
                              '</div></div></div></div>')
                              
    elif test_condition == "header":
        message = random.choice(mindset_messages)
        card.growthHeader = "<p><em>" + message + "</em></p>"

    



        
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
