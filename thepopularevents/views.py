from django.http import HttpResponse, JsonResponse
import settings
import requests

def home_page(request):
    html_code = """
    <html><head><title>The Popular Events</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vue/2.5.6/vue.js"></script>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.19.2/moment.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.4/lodash.min.js"></script>
    <script>
    $(function() {
    function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}
    Vue.component('calendar', {
    props: ['month', 'yearAndMonth', 'dayOfWeek', 'lastDayOfMonthDayOfWeek', 'dayOfMonth', 'endOfMonth', 'eventsByDay'],
    computed: {
      numberOfRows: function() {
        console.log(this.endOfMonth, this.dayOfMonth, this.dayOfWeek)
        return Math.ceil((this.endOfMonth - this.dayOfMonth + this.dayOfWeek + 1) / 7)
      }
    },
    methods: {
    range: function(start, end, step=1) {
    return _.range(start, end, step);
    },
    getDate: function(dayOfMonth) {
    // append 0 to dayOfMonth
    return this.yearAndMonth.format('YYYY-')+this.yearAndMonth.format('MM-')+pad(dayOfMonth, 2);
    }
    },
    template: `<div><h2>{{ month }}</h2>
    <table>
    <tr><th>Sunday</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th>
    <th>Thursday</th><th>Friday</th><th>Saturday</th></tr>
    <tr v-for="vertical_i in range(numberOfRows)">
    <template v-if="vertical_i == 0">
    <td v-for="i in range(dayOfWeek)"></td>
    <calendar-cell v-for="i in range(7-dayOfWeek)" v-bind:year-and-month="yearAndMonth" v-bind:day-of-month="dayOfMonth + i" v-bind:eventsByDay="eventsByDay" key="vertical_i + ',' + i"></calendar-cell>
    </template>
    <template v-else-if="vertical_i == (numberOfRows - 1)">
    <calendar-cell v-for="i in range(lastDayOfMonthDayOfWeek+1)" v-bind:year-and-month="yearAndMonth" v-bind:day-of-month="i + (endOfMonth - lastDayOfMonthDayOfWeek)" v-bind:eventsByDay="eventsByDay" key="vertical_i + ',' + i"></calendar-cell>
    <td v-for="i in range(0, 7-lastDayOfMonthDayOfWeek-1)"></td>
    </template>
    <template v-else>
    <calendar-cell v-for="i in range(7)" v-bind:year-and-month="yearAndMonth" v-bind:day-of-month="(vertical_i) * 7 + i + (dayOfMonth - dayOfWeek)" v-bind:eventsByDay="eventsByDay" key="vertical_i + ',' + i"></calendar-cell>

    </template>
    </tr>
    </table></div>`
    })
    Vue.component('calendar-cell', {
  // The todo-item component now accepts a
  // "prop", which is like a custom attribute.
  // This prop is called todo.
  props: ['dayOfMonth', 'eventsByDay', 'yearAndMonth'],
  methods: {
  range: function(start, end, step=1) {
  return _.range(start, end, step);
  },
  getDate: function(dayOfMonth) {
      console.log('yearAndMonth', this.yearAndMonth)
      console.log('dayOfMonth', dayOfMonth)
  // append 0 to dayOfMonth
  return this.yearAndMonth.format('YYYY-')+this.yearAndMonth.format('MM-')+pad(dayOfMonth, 2);
  }
  },
  template: '<td>{{ dayOfMonth }} <ul><li v-for="event in eventsByDay[getDate(dayOfMonth)]">{{ event.yes_rsvp_count }} attending "<a target="_blank" v-bind:href="event.link">{{ event.group.name }}: {{ event.name }}</a>" at {{ event.local_time }}<template v-if="event.venue"> in {{ event.venue.city }}</template></li></ul></td>'
})
    var app = new Vue({
el: '#app',
data: {
  currentMonth: moment().format('MMMM'),
  yearAndMonth: moment(),
  nextYearAndMonth: moment().add(1, 'months'),
  nextMonth: moment().add(1, 'months').format('MMMM'),
  dayOfWeek: moment().day(),
  nextMonthDayOfWeek: moment().add(1, 'months').startOf('month').day(),
  lastDayOfMonthDayOfWeek: moment().endOf('month').day(),
  nextMonthLastDayOfMonthDayOfWeek: moment().add(1, 'months').endOf('month').day(),
  dayOfMonth: moment().date(),
  endOfMonth: moment().endOf('month').date(),
  nextMonthEndOfMonth: moment().add(1, 'months').startOf('month').endOf('month').date(),
  eventsByDay: {},
  topTenEvents: []
},
created: function() {
$.get('/get_events/', function(data) {
app.eventsByDay = data.most_popular_events_per_day;
app.topTenEvents = data.top_ten_events;
})
},

})
    })

    </script>
<style>
th, td {
vertical-align:top;
border:1px solid #000;
}
table {
border-collapse:collapse;
width:100%;
}
</style>
    </head>
    <body>
    <div id="app">
    <h1>The Popular Events</h1>
    <template v-if="topTenEvents.length > 0">
    <h2>Top Ten Events</h2>
    <ul>
    <li v-for="event in topTenEvents">On {{ event.local_date }} {{ event.yes_rsvp_count }} attending "<a target="_blank" v-bind:href="event.link">{{ event.group.name }}: {{ event.name }}</a>" at {{ event.local_time }}<template v-if="event.venue"> in {{ event.venue.city }}</template></li>
    </ul>
    <calendar v-bind:month="currentMonth" v-bind:year-and-month="yearAndMonth" v-bind:day-of-week="dayOfWeek" v-bind:last-day-of-month-day-of-week="lastDayOfMonthDayOfWeek" v-bind:day-of-month="dayOfMonth" v-bind:end-of-month="endOfMonth" v-bind:events-by-day="eventsByDay"></calendar>
    <calendar v-bind:month="nextMonth" v-bind:year-and-month="nextYearAndMonth" v-bind:day-of-week="nextMonthDayOfWeek" v-bind:last-day-of-month-day-of-week="nextMonthLastDayOfMonthDayOfWeek" v-bind:day-of-month="1" v-bind:end-of-month="nextMonthEndOfMonth" v-bind:events-by-day="eventsByDay"></calendar>
    </template>
    <template v-else>Loading</template>
    </div>
    </body></html>
    """
    return HttpResponse(html_code)

def get_events(request):
    import requests
    if not settings.MEETUPAPIKEY:
        return JsonResponse({'success': False, 'error': 'MEETUPAPIKEY environment variable not set'})

    events_url = 'https://api.meetup.com/find/upcoming_events?page=2000&key=%s&end_date_range=2020-12-30T00:00:00' % (settings.MEETUPAPIKEY)
    print events_url
    events = requests.get(events_url).json()['events']
    top_ten_events = sorted([y for y in events], key=lambda t: t.get('yes_rsvp_count'), reverse=True)[:10]
    days_to_events = dict([(x, sorted([y for y in events if y.get('local_date') == x], key=lambda t: t.get('yes_rsvp_count'), reverse=True)) for x in [row.get("local_date") for row in events]])
    data = {'most_popular_events_per_day': days_to_events, 'top_ten_events': top_ten_events}
    return JsonResponse(data, safe=False)
