from datetime import datetime
from django.utils import timezone
from garnbarn_api.models import Assignment


class GarnBarnMessagingApiFlexMessageGenerator:
    FRONTEND_URI_PREFIX = "https://garnbarn.web.app"

    @staticmethod
    def get_text_color(background_color):
        """Get the text color for the background color

        Args:
            background_color (string): The background color in hex

        Returns:
            string: The text color in hex
        """
        if background_color[0] == "#":
            background_color = background_color[1:]
        r = int(background_color[0:2], 16)
        g = int(background_color[2:4], 16)
        b = int(background_color[4:6], 16)
        if (r * 0.299 + g * 0.587 + b * 0.114) > 186:
            return "#000000"
        else:
            return "#ffffff"

    def generate_title(self, text):
        """Generate the title object for the flex message

        Args:
            text (string): The title text

        Returns:
            Dict: The title flex message object
        """
        return {
            "type": "text",
            "text": text,
            "weight": "bold",
            "size": "xxl",
            "margin": "md",
            "wrap": True,
            "maxLines": 2
        }

    def generate_tag_box(self, text, color):
        """Generate the tag box flex message

        Args:
            text (string): The text in the tag box.
            color (string): The background color in hex

        Returns:
            Dict: The flex message object
        """
        if not color:
            color = "#f9f9f9"
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "Tag:",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "wrap": True,
                    "flex": 1,
                    "align": "center",
                    "gravity": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": text,
                            "color": self.get_text_color(color),
                            "align": "center",
                            "wrap": False
                        }
                    ],
                    "flex": 8,
                    "backgroundColor": color,
                    "borderWidth": "5px",
                    "cornerRadius": "30px",
                    "alignItems": "center",
                    "paddingStart": "5px",
                    "paddingEnd": "5px"
                }
            ],
            "spacing": "3px"
        }

    def generate_due_date(self, date: datetime):
        """Generate the due date flex message
        """
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "Due Date:"
                },
                {
                    "type": "text",
                    "text": date.astimezone(
                        timezone.get_current_timezone()).strftime(
                        "%d %b %Y\n%-I:%M %p"),
                    "wrap": True,
                    "align": "end"
                }
            ],
            "paddingTop": "10px"
        }

    def generate_detail_section(self, text):
        """Generate the detail flex message

        Args:
            text (string): The detail text

        Returns:
            Dict: The detail flex message object
        """
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": text,
                    "maxLines": 20,
                    "wrap": True
                }
            ],
            "paddingTop": "5px"
        }

    def generate_detail_header(self):
        """Generate the detail header flex message

        Returns:
            Dict: The detail header flex message object
        """
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "separator",
                            "margin": "10px"
                        }
                    ],
                    "alignItems": "center",
                    "paddingEnd": "10px",
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": "Detail",
                    "flex": 4,
                    "align": "center",
                    "weight": "bold",
                    "size": "20px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "separator",
                            "margin": "10px"
                        }
                    ],
                    "alignItems": "center",
                    "paddingStart": "10px",
                    "flex": 3
                }
            ],
            "paddingTop": "10px"
        }

    def generate_action_button(self, assignment_id):
        """Generate the action button flex message

        Args:
            assignment_id (string): The assignment id of the targeted assignment
        """
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "View assignment on Garnban",
                        "uri": f"{self.FRONTEND_URI_PREFIX}/assignment/{assignment_id}"
                    },
                    "style": "primary"
                }
            ],
            "paddingTop": "10px"
        }

    def get_assignment_flex_message(self, assignment: Assignment):
        """Generate the Assignment Notification flex message structure

        Args:
            assignment (dict): The assignment object
        """
        contents = []
        contents.append({
            "type": "text",
            "text": "Garnbarn Notification",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },)
        contents.append(self.generate_title(
            text=assignment.assignment_name))
        if assignment.tag:
            contents.append(self.generate_tag_box(
                text=assignment.tag.name, color=assignment.tag.color))
        if assignment.due_date:
            contents.append(self.generate_due_date(date=assignment.due_date))
        if assignment.description:
            contents.append(self.generate_detail_header())
            contents.append(self.generate_detail_section(
                text=assignment.description))
            contents.append({
                "type": "separator",
                "margin": "xxl"
            })
        contents.append(self.generate_action_button(
            assignment_id=assignment.id))
        return {
            "type": "flex",
            "altText": f"Notification of assignment `{assignment.assignment_name}`",
            "contents": {
                "type": "bubble",
                "size": "mega",
                "body": {

                        "type": "box",
                        "layout": "vertical",
                        "contents": contents

                }
            }
        }
