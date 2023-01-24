import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Window 2.15

Window {
    visible: true
    visibility: Window.FullScreen

    width: 1920
    height: 1080

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
                // purpose: rotary_encoder_presentation_model_0.purpose

                Connections {
                    target: rotary_encoder_presentation_model_0

                    function onPushbutton_pressed() {
                        rotary_encoder_0.visualize_pushbutton_pressed()
                    }
                    function onPushbutton_released() {
                        rotary_encoder_0.visualize_pushbutton_released()
                    }
                }
            }

            RotaryEncoder {
                id: rotary_encoder_1
                min: rotary_encoder_presentation_model_1.min
                max: rotary_encoder_presentation_model_1.max
                position: rotary_encoder_presentation_model_1.position
                state: rotary_encoder_presentation_model_1.state

                Connections {
                    target: rotary_encoder_presentation_model_1

                    function onPushbutton_pressed() {
                        rotary_encoder_1.visualize_pushbutton_pressed()
                    }
                    function onPushbutton_released() {
                        rotary_encoder_1.visualize_pushbutton_released()
                    }
                }
            }

            RotaryEncoder {
                id: rotary_encoder_2
                min: rotary_encoder_presentation_model_2.min
                max: rotary_encoder_presentation_model_2.max
                position: rotary_encoder_presentation_model_2.position
                state: rotary_encoder_presentation_model_2.state

                Connections {
                    target: rotary_encoder_presentation_model_2

                    function onPushbutton_pressed() {
                        rotary_encoder_2.visualize_pushbutton_pressed()
                    }
                    function onPushbutton_released() {
                        rotary_encoder_2.visualize_pushbutton_released()
                    }
                }
            }

            RotaryEncoder {
                id: rotary_encoder_3
                min: rotary_encoder_presentation_model_3.min
                max: rotary_encoder_presentation_model_3.max
                position: rotary_encoder_presentation_model_3.position
                state: rotary_encoder_presentation_model_3.state

                Connections {
                    target: rotary_encoder_presentation_model_3

                    function onPushbutton_pressed() {
                        rotary_encoder_3.visualize_pushbutton_pressed()
                    }
                    function onPushbutton_released() {
                        rotary_encoder_3.visualize_pushbutton_released()
                    }
                }
            }

        }
        
    }

}
