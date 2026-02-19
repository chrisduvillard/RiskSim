import streamlit as st
import streamlit.components.v1 as components
from htbuilder import HtmlElement, a, div, hr, p, styles
from htbuilder.units import percent, px


def link(link, text, **style):
    """Create an HTML link element with given href and text."""
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):
    """Layout the footer at the bottom of the Streamlit app."""
    style = """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .stApp { bottom: 80px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        text_align="center",
        height="auto",
        opacity=1,
    )

    style_hr = styles(
        display="block",
        margin=px(0, 0, 0, 0),
        border_style="inset",
        border_width=px(2),
    )

    body = p(
        id="myFooter",
        style=styles(
            margin=px(0, 0, 0, 0),
            padding=px(5),
            font_size="0.8rem",
            color="inherit",
        ),
    )

    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, (str, HtmlElement)):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

    # JS to adapt footer color to Streamlit theme
    js_code = """
    <script>
    function rgbReverse(rgb){
        var r = rgb[0]*0.299;
        var g = rgb[1]*0.587;
        var b = rgb[2]*0.114;
        if ((r + g + b)/255 > 0.5){
            return "rgb(49, 51, 63)"
        } else {
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
                if (pTag) { pTag.style.color = fontColor; }
            });
        });
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
    """
    components.html(js_code)


def footer():
    """Display a footer with a custom message and link."""
    myargs = [
        "Made with ❤️ by ",
        link("https://github.com/chrisduvillard", "Chris"),
    ]
    layout(*myargs)


def metric_box(title: str, value: str) -> str:
    """Return an HTML metric card that adapts to light/dark Streamlit themes."""
    return f"""
    <div style="
        padding: 20px;
        border-radius: 15px;
        background: color-mix(in srgb, currentColor 6%, transparent);
        box-shadow: 0 2px 8px rgba(128, 128, 128, 0.15);
        text-align: center;
        margin: 10px;
        width: 100%;
        font-family: 'Arial', sans-serif;
    ">
        <h4 style="
            color: inherit;
            opacity: 0.7;
            margin-bottom: 12px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        ">{title}</h4>
        <p style="
            font-size: 20px;
            font-weight: bold;
            color: inherit;
            margin: 0;
        ">{value}</p>
    </div>
    """
