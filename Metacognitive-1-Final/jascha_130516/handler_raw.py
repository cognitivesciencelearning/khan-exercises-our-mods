import urllib

import request_handler
import user_util
import experiments
import os
from exercises import file_contents
from exercises import file_experiments


class RawExercise(request_handler.RequestHandler):

    def metacog_filename_map(self, filename):
        """
        serve up an alternative version of the exercise as appropriate
        for the metacognitive experiment.

        (note that we're not using file_experiments.py since we want the
        experimental conditions to be consistent across multiple exercises,
        and because there are more experimental conditions than are supported
        in a single bingo experiment)
        """

        target_filenames = [
            'linear_equations_3.html',
            'linear_equation_word_problems.html'
        ]

        if False: #filename not in target_filenames:
            return filename

        test_condition = experiments.CoreMetrics.ab_test("metacognitive 1",
            alternative_params={
                "control": 3,
                "what why how": 1},
            core_categories='all')

        if True: #test_condition == 'control':
            return filename

        # which variation of the study strategy questions to present to
        # the students
        test_condition_1 = experiments.CoreMetrics.ab_test(
            "metacognitive 1 prompt type",
            alternative_params={
                "control": 98,
                "reflectingonmeaning": 99,
                "selfregulatingthinking": 100},
            core_categories='all')
        test_condition_1 = "control"

        # whether or not there are additional textboxes in the hints for
        # the students to answer the questions in
        test_condition_2 = experiments.CoreMetrics.ab_test(
            "metacognitive 1 text",
            alternative_params={
                "textbox": 99,
                "notextbox": 100},
            core_categories='all')
        test_condition_2 = 'textbox'

        # modify the filename based on the experimental conditions the
        # student is in
        base, extension = os.path.splitext(filename)
        return base + '_' + test_condition_1 + '_' + test_condition_2 + extension

    @user_util.open_access
    def get(self):
        """Return the raw HTML contents of requested exercise file.

        Note that we don't set any cache headers for this static response,
        because we frequently push bug fixes for these files and want them to
        be updated immediately. Letting downstream caches hold our content
        would also cause problems for the a/b tests in
        exercises.file_experiments.
        """
        path = self.request.path
        filename = urllib.unquote(path.split('/', 3)[3])

        # enter the user into the metacognitive experiment, if appropriate
        filename = self.metacog_filename_map(filename)
        # NOTE Any file_experiments will be performed on the control version
        # of this exercise, which has its filename unchanged. Need to watch out
        # for file_experiments when interpreting the data.

        # If this exercise is in an experiment, get the current user's possibly
        # modified filename for their exercise content alternative.
        file_experiment = file_experiments.get_experiment(filename)
        if file_experiment:
            filename = file_experiment.filename_for_current_user()

        language = self.request_language_tag()
        contents = file_contents.raw_exercise_contents(filename, language)

        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write(contents)
