import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Window 2.15

Window {
    visible: true
    visibility: Window.FullScreen

    width: 1920
    height: 1080

    property string darker_color: "#1b1b1b"

    // BACKGROUND
    Rectangle {
        id: main_background
        anchors.fill: parent

        Image {
            anchors.fill: parent
            source: "Background.png"
            fillMode: Image.PreserveAspectCrop
        }
    }
    

    Item {
        id: root
        anchors.fill: parent

        Row {
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 2
            anchors.right: parent.right
            anchors.rightMargin: 2
            
            spacing: 12

            RotaryEncoder {
                id: rotary_encoder_0
                min: rotary_encoder_presentation_model_0.min
                max: rotary_encoder_presentation_model_0.max
                position: rotary_encoder_presentation_model_0.position
                state: rotary_encoder_presentation_model_0.state
            }

            RotaryEncoder {
                id: rotary_encoder_1
                min: rotary_encoder_presentation_model_1.min
                max: rotary_encoder_presentation_model_1.max
                position: rotary_encoder_presentation_model_1.position
                state: rotary_encoder_presentation_model_1.state
            }

            RotaryEncoder {
                id: rotary_encoder_2
                min: rotary_encoder_presentation_model_2.min
                max: rotary_encoder_presentation_model_2.max
                position: rotary_encoder_presentation_model_2.position
                state: rotary_encoder_presentation_model_2.state
            }

            RotaryEncoder {
                id: rotary_encoder_3
                min: rotary_encoder_presentation_model_3.min
                max: rotary_encoder_presentation_model_3.max
                position: rotary_encoder_presentation_model_3.position
                state: rotary_encoder_presentation_model_3.state
            }

        }

        // ColorPicker 
        ColorPicker {
            property var last_rotary_encoder_0_position: rotary_encoder_0.position
            property var last_rotary_encoder_1_position: rotary_encoder_1.position
            property var last_rotary_encoder_2_position: rotary_encoder_2.position
            property var last_rotary_encoder_3_position: rotary_encoder_3.position
                    
            id: color_picker
            visible: false
            anchors.centerIn: parent

            r: rotary_encoder_0.position
            g: rotary_encoder_1.position
            b: rotary_encoder_2.position
            a: rotary_encoder_3.position

            onVisibleChanged: {
                if (color_picker.visible == true) {
                    rotary_encoder_0.purpose = "Red"
                    rotary_encoder_1.purpose = "Green"
                    rotary_encoder_2.purpose = "Blue"
                    rotary_encoder_3.purpose = "Dimmer"

                    rotary_encoder_0.position = last_rotary_encoder_0_position
                    rotary_encoder_1.position = last_rotary_encoder_1_position
                    rotary_encoder_2.position = last_rotary_encoder_2_position
                    rotary_encoder_3.position = last_rotary_encoder_3_position

                    console.log("ColorPicker Opened")

                } else {
                    rotary_encoder_0.purpose = "---"
                    rotary_encoder_1.purpose = "---"
                    rotary_encoder_2.purpose = "---"
                    rotary_encoder_3.purpose = "---"

                    last_rotary_encoder_0_position = rotary_encoder_0.position
                    last_rotary_encoder_1_position = rotary_encoder_1.position
                    last_rotary_encoder_2_position = rotary_encoder_2.position
                    last_rotary_encoder_3_position = rotary_encoder_3.position

                    rotary_encoder_0.position = 0
                    rotary_encoder_1.position = 0
                    rotary_encoder_2.position = 0
                    rotary_encoder_3.position = 0

                    console.log("ColorPicker Closed")
                }
            }
        }


        // SideBar Selector
        GridLayout {
            id: side_bar_selector
            anchors.right: parent.right
            anchors.rightMargin: 2
            anchors.top: parent.top
            anchors.topMargin: 2
            Column {
                Rectangle {
                    width: 90
                    height: 90
                    color: darker_color

                    Text {
                        anchors.centerIn: parent
                        text: "RGB"
                        font.pixelSize: 30
                        font.family: "TW Cen MT"
                        color: "white"
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (color_picker.visible == true) {
                                color_picker.visible = false
                            } else {
                                color_picker.visible = true
                            }
                        }
                    }
                }
            }
        }

        
        
    }

}
