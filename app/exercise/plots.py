import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from app.models import User, Streak
from matplotlib.ticker import MaxNLocator

def create_streak_plt(streaks: list) -> str:
    """Creates an encoded graph image from a list of streak objects and returns it"""

    highest_streaks = dict()

    for streak in streaks:
        highest_streaks.update({streak.old_user: 0})

    for streak in streaks:
        if highest_streaks[streak.old_user] < streak.total_count:
            highest_streaks[streak.old_user] = streak.total_count

    sorted_streaks = sorted(highest_streaks.items(), key=lambda item: item[1], reverse=True)
    user_list = []
    count_list = []

    top_num = 5
    bottom_num = 0
    for user, count in sorted_streaks:
        user_list.append(user)
        count_list.append(count)
        bottom_num += 1
        if bottom_num == top_num:
            break

    # Generate plot
    fig = Figure()
    axis = fig.add_subplot(111)
    axis.bar(user_list, count_list)
    # axis.bar([user for user in highest_streaks.keys()], highest_streaks.values())
    axis.set_title("Top {} Streaks".format(top_num))
    axis.set_ylabel("Highest Streak")
    y_ax = axis.axes.get_yaxis()
    y_ax.set_major_locator(MaxNLocator(integer=True))

    # Convert plot to PNG image
    png_image = io.BytesIO()
    FigureCanvas(fig).print_png(png_image)

    # Encode PNG image to base64 string
    png_image_encoded = "data:image/png;base64,"
    png_image_encoded += base64.b64encode(png_image.getvalue()).decode('utf8')

    return png_image_encoded
