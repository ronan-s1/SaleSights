from datetime import datetime


# display a custom styled container for each service
def service_container(iconname, i, sline):
    wch_colour_box = (233, 236, 251)
    wch_colour_font = (4, 9, 33)
    fontsize = 22

    html_template = f"""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous">
        <p style='background-color: rgba({wch_colour_box[0]}, {wch_colour_box[1]}, {wch_colour_box[2]}, 0.75);
            color: rgba({wch_colour_font[0]}, {wch_colour_font[1]}, {wch_colour_font[2]}, 0.8);
            font-size: {fontsize}px;
            border-radius: 7px;
            padding-left: 12px;
            padding-top: 18px;
            padding-bottom: 18px;
            line-height: 25px;'>
            <i class='{iconname} fa-2xs'></i> {i}
            </br>
            <span style='font-size: 14px; margin-top: 0;'>{sline}</span>
        </p>
    """
    return html_template


# get greeting depending on hour of the day
def get_greeting():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning ☀️"
    elif 12 <= current_hour < 18:
        return "Good afternoon 🌤️"

    return "Good evening 🌙"
