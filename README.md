# Some easy dash apps

Each app can be used by running `python app.py`.

## App 1

Simple dashboard with standard HTML layout and some inputs and outputs through callbacks interactions.

## App 2

App with bootstrap layout syntax and a few more interactions (buttons, sliders, dropdown menu)

## App 3

A main plot where you can select countries and the two axae. On the right, a scatter plot about a country you can hover on from the main plot, and a histogram for all countries selected in the main plot (selection happens by box selection or shift+click selection) across all years.

## App 4

Works as in App 3 with an additional plot. This plot is a histogram of average life expectancy for either countries or continents. The two types of averages are calculated by a callback and stored in json format, so that you perform the calculations only once and do not need to do it all the time (useful for expensive calculations). To so this, you add the intermediate json values as inputs in the callback that produces the histogram, and you have another callback specifically triggering the calculations (for example by choosing country/continent on the dropdown, triggering those calculations which will be stored as json file).