// Example usage:
// <var>person(1)</var> traveled 5 mi by <var>vehicle(1)</var>. Let
// <var>his(1)</var> average speed be <var>personVar(1)</var>.
// Let <var>person(2)</var>'s speed be <var>personVar(2)</var>.
//
// Note that initials (-Var) are guaranteed to be unique in each category,
// but not across them.

$.extend(KhanUtil, {
    // TODO(jeresig): i18n: Figure out how this should be converted
    toSentence: function(array, conjunction) {
        if (conjunction == null) {
            conjunction = "and";
        }

        if (array.length === 0) {
            return "";
        } else if (array.length === 1) {
            return array[0];
        } else if (array.length === 2) {
            return array[0] + " " + conjunction + " " + array[1];
        } else {
            return array.slice(0, -1).join(", ") + ", " + conjunction + " " + array[array.length - 1];
        }
    },

    toSentenceTex: function(array, conjunction, highlight, highlightClass) {
        var wrapped = $.map(array, function(elem) {
            if (($.isFunction(highlight) && highlight(elem)) || (highlight !== undefined && elem === highlight)) {
                return "<code class='" + highlightClass + "'>" + elem + "</code>";
            }
            return "<code>" + elem + "</code>";
        });
        return KhanUtil.toSentence(wrapped, conjunction);
    },

    capitalize: function(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    },

    // NOTE(jeresig): If you want to pluralize a word you must add it here!
    // Look-up table of plural word translations culled from exercise files
    // Makes it possible to actually extract these words for i18n
    plurals: {
        "apple": function(num) {
            return $.ngettext("apple", "apples", num);
        },
        "banana": function(num) {
            return $.ngettext("banana", "bananas", num);
        },
        "basket": function(num) {
            return $.ngettext("basket", "baskets", num);
        },
        "car": function(num) {
            return $.ngettext("car", "cars", num);
        },
        "circle": function(num) {
            return $.ngettext("circle", "circles", num);
        },
        "coconut": function(num) {
            return $.ngettext("coconut", "coconuts", num);
        },
        "eggplant": function(num) {
            return $.ngettext("eggplant", "eggplants", num);
        },
        "foot": function(num) {
            return $.ngettext("foot", "feet", num);
        },
        "kilometer": function(num) {
            return $.ngettext("kilometer", "kilometers", num);
        },
        "kiwi": function(num) {
            return $.ngettext("kiwi", "kiwis", num);
        },
        "lemon": function(num) {
            return $.ngettext("lemon", "lemons", num);
        },
        "loaf": function(num) {
            return $.ngettext("loaf", "loaves", num);
        },
        "mango": function(num) {
            return $.ngettext("mango", "mangos", num);
        },
        "mile": function(num) {
            return $.ngettext("mile", "miles", num);
        },
        "nectarine": function(num) {
            return $.ngettext("nectarine", "nectarines", num);
        },
        "orange": function(num) {
            return $.ngettext("orange", "oranges", num);
        },
        "package": function(num) {
            return $.ngettext("package", "packages", num);
        },
        "piece": function(num) {
            return $.ngettext("piece", "pieces", num);
        },
        "pomegranate": function(num) {
            return $.ngettext("pomegranate", "pomegranates", num);
        },
        "potato": function(num) {
            return $.ngettext("potato", "potatoes", num);
        },
        "push-up": function(num) {
            return $.ngettext("push-up", "push-ups", num);
        },
        "row": function(num) {
            return $.ngettext("row", "rows", num);
        },
        "sit-up": function(num) {
            return $.ngettext("sit-up", "sit-ups", num);
        },
        "squat": function(num) {
            return $.ngettext("squat", "squats", num);
        },
        "quiz": function(num) {
            return $.ngettext("quiz", "quizzes", num);
        },
        "shelf": function(num) {
            return $.ngettext("shelf", "shelves", num);
        },
        "square foot": function(num) {
            return $.ngettext("square foot", "square feet", num);
        },
        "team": function(num) {
            return $.ngettext("team", "teams", num);
        },
        "tomato": function(num) {
            return $.ngettext("tomato", "tomatoes", num);
        },
        "watermelon": function(num) {
            return $.ngettext("watermelon", "watermelons", num);
        }
    },

    plural_form: function(word, num) {
        // There are some cases where plural_form is called with only a word
        // (and no number). In this case we just want to return the plural
        // form of that word, as best as we can. This might have some slight
        // incongruities across platforms
        num = num === undefined ? 2 : num;

        if (word && "plural_fn" in word) {
            return word.plural_fn(num);
        }

        if (word in KhanUtil.plurals) {
            return KhanUtil.plurals[word](num);
        }

        // TODO(jeresig): i18n: Eventually remove this?
        if (typeof console !== "undefined" && console.error) {
            console.error("Word not in plural dictionary: ", word);
        }

        return word;
    },

    isSingular: function(num) {
        return num == 1;
    },

    // DEPRECATED
    // pluralization helper.  There are two signatures
    // - plural(NUMBER, singular):
    //        - if necessary, magically pluralize <singular>
    //        - return "NUMBER word"
    // - plural(NUMBER, singular, plural):
    //        - return "NUMBER word"
    // - plural(singular, NUMBER):
    //        - if necessary, magically pluralize <singular>
    //        - return "word"
    // - plural(singular, plural, NUMBER):
    //        - return "word"
    plural: (function() {
        var oneOffs = {
            "quiz": "quizzes",
            "shelf": "shelves",
            "loaf": "loaves",
            "potato": "potatoes",
            "person": "people",
            "is": "are",
            "was": "were",
            "foot": "feet",
            "square foot": "square feet",
            "tomato": "tomatoes"
        };

        var pluralizeWord = function(word) {

            // noone really needs extra spaces at the edges, do they?
            word = $.trim(word);

            // determine if our word is all caps.  If so, we'll need to
            // re-capitalize at the end
            var isUpperCase = (word.toUpperCase() === word);
            var oneOff = oneOffs[word.toLowerCase()];
            var words = word.split(/\s+/);

            // first handle simple one-offs
            // ({}).watch is a function in Firefox, blargh
            if (typeof oneOff === "string") {
                return oneOff;
            }

            // multiple words
            else if (words.length > 1) {
                // for 3-word phrases where the middle word is 'in' or 'of',
                // pluralize the first word
                if (words.length === 3 && /\b(in|of)\b/i.test(words[1])) {
                    words[0] = KhanUtil.plural(words[0]);
                }

                // otherwise, just pluraize the last word
                else {
                    words[words.length - 1] =
                        KhanUtil.plural(words[words.length - 1]);
                }

                return words.join(" ");
            }

            // single words
            else {
                // "-y" => "-ies"
                if (/[^aeiou]y$/i.test(word)) {
                    word = word.replace(/y$/i, "ies");
                }

                // add "es"; things like "fish" => "fishes"
                else if (/[sxz]$/i.test(word) || /[bcfhjlmnqsvwxyz]h$/.test(word)) {
                    word += "es";
                }

                // all the rest, just add "s"
                else {
                    word += "s";
                }

                if (isUpperCase) {
                    word = word.toUpperCase();
                }
                return word;
            }
        };

        return function(value, arg1, arg2) {
            if (typeof value === "number") {
                var usePlural = (value !== 1);

                // if no extra args, just add "s" (if plural)
                if (arguments.length === 1) {
                    return usePlural ? "s" : "";
                }

                if (usePlural) {
                    arg1 = arg2 || pluralizeWord(arg1);
                }

                return value + " " + arg1;
            } else if (typeof value === "string") {
                var plural = pluralizeWord(value);
                if (typeof arg1 === "string" && arguments.length === 3) {
                    plural = arg1;
                    arg1 = arg2;
                }
                var usePlural = (arguments.length < 2 || (typeof arg1 === "number" && arg1 !== 1));
                return usePlural ? plural : value;
            }
        };
    })(),

    // Pluralize with a code tag around the number
    // - pluralTex(NUMBER, singular):
    //        - if necessary, magically pluralize <singular>
    //        - return "<code>NUMBER</code> word"
    // - pluralTex(NUMBER, singular, plural):
    //        - return "<code>NUMBER</code> word"
    pluralTex: function(value, arg1, arg2) {
        if (typeof arg2 === "string") {
            return "<code>" + value + "</code> " + KhanUtil.plural(arg1, arg2, value);
        } else {
            return "<code>" + value + "</code> " + KhanUtil.plural(arg1, value);
        }
    }
});

KhanUtil.Plural = function(plural_fn) {
    this.plural_fn = plural_fn;
};

KhanUtil.Plural.prototype = {
    toString: function() {
        return this.plural_fn(1);
    }
};

$.fn["word-problemsLoad"] = function() {

    var IncrementalShuffler = function(array) {
        // Shuffle an array incrementally so we only use as many random calls
        // as we need, so names can be added/removed without breaking all
        // random seeds for all word problems
        // - get(0); get(0); will use only one call
        // - get(0); get(1); will have each use one random call
        // - get(1); get(0); will use two random calls then none and each call
        //   will give the same result as running 0 then 1
        array = [].slice.call(array, 0);
        var shuffled = 0;

        this.get = function(i) {
            if (i < 0 || i >= array.length) {
                return undefined;
            }

            while (shuffled <= i) {
                var top = array.length - shuffled,
                    newEnd = Math.floor(KhanUtil.random() * top),
                    tmp = array[newEnd];

                array[newEnd] = array[top - 1];
                array[top - 1] = tmp;
                shuffled++;
            }

            // Since we shuffle items from the end to the front, return the
            // items in reverse order
            return array[array.length - i - 1];
        };
    };

    var names = [
        // I18N: Female name
        [$._("Ashley"), "f"],
        // I18N: Male name
        [$._("Brandon"), "m"],
        // I18N: Male name
        [$._("Ben"), "m"],
        // I18N: Male name
        [$._("Christopher"), "m"],
        // I18N: Male name
        [$._("Daniel"), "m"],
        // I18N: Female name
        [$._("Emily"), "f"],
        // I18N: Female name
        [$._("Gabriela"), "f"],
        // I18N: Male name
        [$._("Ishaan"), "m"],
        // I18N: Female name
        [$._("Jessica"), "f"],
        // I18N: Male name
        [$._("Kevin"), "m"],
        // I18N: Male name
        [$._("Luis"), "m"],
        // I18N: Male name
        [$._("Michael"), "m"],
        // I18N: Female name
        [$._("Nadia"), "f"],
        // I18N: Male name
        [$._("Omar"), "m"],
        // I18N: Female name
        [$._("Stephanie"), "f"],
        // I18N: Female name
        [$._("Tiffany"), "f"],
        // I18N: Female name
        [$._("Umaima"), "f"],
        // I18N: Female name
        [$._("Vanessa"), "f"],
        // I18N: Male name
        [$._("William"), "m"]
    ];

    // We only want one name per letter of the alphabet, so group people with
    // the same initial before shuffling the names up
    var people = _.map(_.groupBy(names, function(name) {
        return name[0].charAt(0);
    }), function(group) {
        return new IncrementalShuffler(group);
    });
    people = new IncrementalShuffler(people);

    // NOTE(jeresig): I18N: These strings are expected to work prefixed with
    // just the letter "A", as in "A gorilla"
    var vehicles = new IncrementalShuffler([
        "bike",
        "car",
        "horse",
        "motorcycle",
        "scooter",
        "train"
    ]);

    // NOTE(jeresig): I18N: These strings are expected to work prefixed with
    // just the letter "A", as in "A gorilla"
    var courses = new IncrementalShuffler([
        "chemistry",
        "geometry",
        "history",
        "mathematics",
        "physics",
        "Spanish"
    ]);

    var exams = new IncrementalShuffler([
        "exam",
        "test",
        "quiz"
    ]);

    var binops = new IncrementalShuffler([
        "\\barwedge",
        "\\veebar",
        "\\odot",
        "\\oplus",
        "\\otimes",
        "\\oslash",
        "\\circledcirc",
        "\\boxdot",
        "\\bigtriangleup",
        "\\bigtriangledown",
        "\\dagger",
        "\\diamond",
        "\\star",
        "\\triangleleft",
        "\\triangleright"
    ]);

    var collections = new IncrementalShuffler([
        ["party favor", "bag"],
        ["jelly bean", "bag"],
        ["book", "shelf"],
        ["can of food", "box"]
    ]);

    // NOTE(jeresig): I18N: These strings are expected to work prefixed with
    // just the letter "A", as in "A gorilla"
    var stores = new IncrementalShuffler([
        {
            name: "hardware",
            items: new IncrementalShuffler(["hammer", "nail", "saw"])
        },
        {
            name: "grocery",
            items: new IncrementalShuffler(["banana", "loaf of bread", "gallon of milk", "potato"])
        },
        {
            name: "gift",
            items: new IncrementalShuffler(["toy", "game", "souvenir"])
        },
        {
            name: "school supply",
            items: new IncrementalShuffler(["pen", "pencil", "notebook"])
        },
        {
            name: "toy",
            items: new IncrementalShuffler(["stuffed animal", "video game", "race car", "doll"])
        }
    ]);

    var pizzas = new IncrementalShuffler([
        "pizza",
        "pie",
        "cake"
    ]);

    var timesofday = new IncrementalShuffler([
        "in the morning",
        "around noon",
        "in the evening",
        "at night"
    ]);

    var exercises = new IncrementalShuffler([
        "push-up",
        "sit-up",
        "squat",
        "jumping jack"
    ]);

    var fruits = new IncrementalShuffler([
        "apple",
        "banana",
        "coconut",
        "eggplant",
        "kiwi",
        "lemon",
        "mango",
        "nectarine",
        "orange",
        "pomegranate",
        "watermelon"
    ]);

    var deskItems = new IncrementalShuffler([
        "binder",
        "crayon",
        "eraser",
        "folder",
        "glue stick",
        "marker",
        "notebook",
        "pencil",
        "rubber stamp"
    ]);

    // NOTE(jeresig): I18N: These strings are expected to work prefixed with
    // just the letter "A", as in "A gorilla"
    var colors = new IncrementalShuffler([
        "red",
        // NOTE(jeresig): I18N: Removed because it begins with a vowel and is
        // used with an()
        //"orange",
        "yellow",
        "green",
        "blue",
        "purple",
        "white",
        "black",
        "brown",
        "silver",
        "gold",
        "pink"
    ]);

    var schools = new IncrementalShuffler([
        "Loyola",
        "Gardner Bullis",
        "Almond",
        "Covington",
        "Springer",
        "Santa Rita",
        "Oak"
    ]);

    var furnitureStore = new IncrementalShuffler([
        "chair",
        "table",
        "bed frame",
        "sofa",
        "couch",
        "desk",
        "book shelf"
    ]);

    var electronicStore = new IncrementalShuffler([
        "television",
        "computer",
        "laptop",
        "camera"
    ]);

    var clothes = new IncrementalShuffler([
        "hat",
        "pair of pants",
        "belt",
        "necklace",
        "purse",
        "pair of shoes",
        "blouse",
        "skirt",
        "watch",
        "pair of socks",
        "sweatshirt",
        "sweater",
        "tie",
        "scarf",
        "dress"
    ]);

    var sides = new IncrementalShuffler([
        "left",
        "right"
    ]);

    var shirtStyles = new IncrementalShuffler([
        "long-sleeved",
        "short-sleeved"
    ]);

    // animal, avg-lifespan, stddev-lifespan
    // (data is from cursory google searches and wild guessing)
    // NOTE(jeresig): I18N: These strings are expected to work prefixed with
    // just the letter "A", as in "A gorilla"
    var animals = new IncrementalShuffler([
        // NOTE(jeresig): I18N: Removed because it begins with a vowel and is
        // used with an()
        //["alligator", 68, 20],
        //["anteater", 15, 10],
        ["bear", 40, 20],
        //["elephant", 60, 10],
        ["gorilla", 20, 5],
        ["lion", 12, 5],
        ["lizard", 3, 1],
        ["meerkat", 13, 5],
        ["porcupine", 20, 5],
        ["seal", 15, 10],
        ["sloth", 16, 5],
        ["snake", 25, 10],
        ["tiger", 22, 5],
        ["turtle", 100, 20],
        ["zebra", 25, 10]
    ]);

    var farmers = new IncrementalShuffler([
        {farmer: "farmer", crops: new IncrementalShuffler(["tomato", "potato", "carrot", "bean", "corn stalk"]), field: "field"},
        {farmer: "gardener", crops: new IncrementalShuffler(["rose", "tulip", "daisy", "iris", "lily"]), field: "garden"}
    ]);

    var distances = new IncrementalShuffler([
        "mile",
        "kilometer"
    ]);

    var distanceActivities = new IncrementalShuffler([
        {present: "ride", past: "rode", noun: "bike", done: "biked", continuous: "biking"},
        {present: "row", past: "rowed", noun: "boat", done: "rowed", continuous: "rowing"},
        {present: "drive", past: "drove", noun: "car", done: "driven", continuous: "driving"},
        {present: "walk", past: "walked", noun: "dog", done: "walked", continuous: "walking"}
    ]);

    var indefiniteArticle = function(word) {
        var vowels = ["a", "e", "i", "o", "u"];
        if (_(vowels).indexOf(word[0].toLowerCase()) > -1) {
            return "An " + word;
        }
        return "A " + word;
    };

    $.extend(KhanUtil, {
        person: function(i) {
            return people.get(i - 1).get(0)[0];
        },

        personVar: function(i) {
            return people.get(i - 1).get(0)[0].charAt(0).toLowerCase();
        },

        he: function(i) {
            return people.get(i - 1).get(0)[1] === "m" ? "he" : "she";
        },

        He: function(i) {
            return people.get(i - 1).get(0)[1] === "m" ? "He" : "She";
        },

        him: function(i) {
            return people.get(i - 1).get(0)[1] === "m" ? "him" : "her";
        },

        his: function(i) {
            return people.get(i - 1).get(0)[1] === "m" ? "his" : "her";
        },

        His: function(i) {
            return people.get(i - 1).get(0)[1] === "m" ? "His" : "Her";
        },

        isMale: function(i) {
            return people.get(i - 1).get(0)[1] === "m";
        },

        An: function(word) {
            return indefiniteArticle(word);
        },

        an: function(word) {
            return indefiniteArticle(word).toLowerCase();
        },

        vehicle: function(i) {
            return vehicles.get(i - 1);
        },

        vehicleVar: function(i) {
            return vehicles.get(i - 1).charAt(0);
        },

        course: function(i) {
            return courses.get(i - 1);
        },

        courseVar: function(i) {
            return courses.get(i - 1).charAt(0).toLowerCase();
        },

        exam: function(i) {
            return exams.get(i - 1);
        },

        binop: function(i) {
            return binops.get(i - 1);
        },

        item: function(i) {
            return collections.get(i - 1)[0];
        },

        group: function(i) {
            return collections.get(i - 1)[1];
        },

        store: function(i) {
            return stores.get(i).name;
        },

        storeItem: function(i, j) {
            return stores.get(i).items.get(j);
        },

        pizza: function(i) {
            return pizzas.get(i);
        },

        exercise: function(i) {
            return exercises.get(i - 1);
        },

        timeofday: function(i) {
            return timesofday.get(i - 1);
        },

        school: function(i) {
            return schools.get(i - 1);
        },

        clothing: function(i) {
            return clothes.get(i - 1);
        },

        color: function(i) {
            return colors.get(i - 1);
        },

        fruit: function(i) {
            return fruits.get(i);
        },

        deskItem: function(i) {
            return deskItems.get(i);
        },

        distance: function(i) {
            return distances.get(i - 1);
        },

        rode: function(i) {
            return distanceActivities.get(i - 1).past;
        },

        ride: function(i) {
            return distanceActivities.get(i - 1).present;
        },

        bike: function(i) {
            return distanceActivities.get(i - 1).noun;
        },

        biked: function(i) {
            return distanceActivities.get(i - 1).done;
        },

        biking: function(i) {
            return distanceActivities.get(i - 1).continuous;
        },

        farmer: function(i) {
            return farmers.get(i - 1).farmer;
        },

        crop: function(i) {
            return farmers.get(i - 1).crops.get(0);
        },

        field: function(i) {
            return farmers.get(i - 1).field;
        },

        side: function(i) {
            return sides.get(i - 1);
        },

        shirtStyle: function(i) {
            return shirtStyles.get(i - 1);
        },

        furniture: function(i) {
            return furnitureStore.get(i - 1);
        },

        electronic: function(i) {
            return electronicStore.get(i - 1);
        },

        animal: function(i) {
            return animals.get(i - 1)[0];
        },

        animalAvgLifespan: function(i) {
            return animals.get(i - 1)[1];
        },

        animalStddevLifespan: function(i) {
            return animals.get(i - 1)[2];
        }
    });
};
