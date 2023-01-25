import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Window {
    visible: true
    visibility: Window.FullScreen

    Item {
        id: root
        anchors.fill: parent

        KKeypad {
            id: kKeypad
            model: kKeypadQmlPresentationModel
        }

        Rectangle {
            id: led_toggle_button
            anchors.centerIn: parent
            width: 200
            height: 200
            color: "red"

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    hardwareLedQmlPresentationModel.change_led_color(0, 255, 255, 0)
                }
            }
        }

        // // DEBUG
        // Rectangle {
        //     anchors.fill: parent
        //     color: "red"
        //     opacity: 0.3
        // }
        // Rectangle {
        //     anchors.fill: parent
        //     border.color: "yellow"
        //     border.width: 1
        //     color: "transparent"
        // }
    }

}
