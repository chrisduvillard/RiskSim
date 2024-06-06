import streamlit as st
import streamlit.components.v1 as components
from htbuilder import HtmlElement, div, hr, a, p, styles
from htbuilder.units import percent, px


def link(link, text, **style):
    """
    Create an HTML link element with given href and text.

    Args:
        link (str): The URL the link points to.
        text (str): The text to display for the link.
        **style: Additional CSS styles to apply to the link.

    Returns:
        HtmlElement: An HTML 'a' element.
    """
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):
    """
    Layout the footer at the bottom of the Streamlit app and inject custom JavaScript.

    Args:
        *args: Variable length argument list to include strings or HtmlElement objects in the footer.
    """
    style = """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .stApp { bottom: 80px; }
    </style>
    """

    # Define styles for the footer container and horizontal line
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(0, 0, 0, 0),
        border_style="inset",
        border_width=px(2)
    )

    # Create the footer body
    body = p(
        id='myFooter',
        style=styles(
            margin=px(0, 0, 0, 0),
            padding=px(5),
            font_size="0.8rem",
            color="rgb(51,51,51)"
        )
    )

    # Combine the elements into the footer div
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    # Inject the custom style into the Streamlit app
    st.markdown(style, unsafe_allow_html=True)

    # Add the provided arguments to the body of the footer
    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    # Render the footer in the Streamlit app
    st.markdown(str(foot), unsafe_allow_html=True)

    # JavaScript code to dynamically change the footer text color based on the background color
    js_code = '''
    <script>
    function rgbReverse(rgb){
        var r = rgb[0]*0.299;
        var g = rgb[1]*0.587;
        var b = rgb[2]*0.114;

        if ((r + g + b)/255 > 0.5){
            return "rgb(49, 51, 63)"
        }else{
            return "rgb(250, 250, 250)"
        }

    };
    var stApp_css = window.parent.document.querySelector("#root > div:nth-child(1) > div > div > div");
    window.onload = function () {
        var mutationObserver = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    var bgColor = window.getComputedStyle(stApp_css).backgroundColor.replace("rgb(", "").replace(")", "").split(", ");
                    var fontColor = rgbReverse(bgColor);
                    var pTag = window.parent.document.getElementById("myFooter");
                    pTag.style.color = fontColor.
                });
            });

            /**Element**/
            mutationObserver.observe(stApp_css, {
                attributes: true,
                characterData: true,
                childList: true,
                subtree: true,
                attributeOldValue: true,
                characterDataOldValue: true
            });
    }
    </script>
    '''
    # Inject the JavaScript code into the Streamlit app
    components.html(js_code)


def footer():
    """
    Display a footer with a custom message and link.
    """
    myargs = [
        "Made with ❤️ by ",
        link("https://github.com/chrisduvillard", "Chris"),
        # " - Stay alive long enough to get lucky - Jason Shapiro",
    ]
    layout(*myargs)


def metric_box(title, value):
    return f"""
    <div style="
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 10px;
        width: 100%;
        font-family: 'Arial', sans-serif;
        transition: transform 0.2s ease-in-out;
    ">
        <h4 style="
            color: #333333;
            margin-bottom: 12px;
            font-size: 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
        ">{title}</h4>
        <p style="
            font-size: 18px;
            font-weight: bold;
            color: #123524;
            margin: 0;
        ">{value}</p>
    </div>
    """
