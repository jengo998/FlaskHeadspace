import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def create_item_plt(prices: list, item_name: str) -> str:
    """Creates an encoded graph image from a list of prices and returns it"""

    sorted_prices = sorted(prices, reverse=True)

    # Generate plot
    fig = Figure()
    axis = fig.add_subplot(111)
    axis.plot(sorted_prices)
    axis.set_title("Recent {} {} sold around this price range".format(len(prices), item_name))
    axis.set_ylabel("Prices in USD")
    axis.set_xlabel("Item Ranking: Highest to Lowest Price")

    # Convert plot to PNG image
    png_image = io.BytesIO()
    FigureCanvas(fig).print_png(png_image)

    # Encode PNG image to base64 string
    png_image_encoded = "data:image/png;base64,"
    png_image_encoded += base64.b64encode(png_image.getvalue()).decode('utf8')

    return png_image_encoded
