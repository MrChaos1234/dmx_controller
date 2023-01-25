import QtQuick 2.15
import QtQuick.Window 2.15

Item {
    id: kKeypad
    property var model: None
    width: 474
    height: 50

    Connections {
        target: model

        function onKey_pressed(key_number) {
            kKeypad.visualizeKeyPressed(key_number)
        }
        function onKey_released(key_number) {
            kKeypad.visualizeKeyReleased(key_number)
        }
    }

    function visualizeKeyPressed(keyNumber) {
        keyNumberDisplay.text = keyNumber.toString()
        keyPressedDisplay.color = "red"
        visualizeKeyPressedTimer.restart()
    }
    function visualizeKeyReleased(keyNumber) {
        keyNumberDisplay.text = keyNumber.toString()
        keyReleasedDisplay.color = "brown"
        visualizeKeyReleasedTimer.restart()
    }

    Timer {
        id: visualizeKeyPressedTimer
        interval: 500
        onTriggered: keyPressedDisplay.color = "white"
    }

    Timer {
        id: visualizeKeyReleasedTimer
        interval: 500
        onTriggered: keyReleasedDisplay.color = "white"
    }

    Rectangle {
        id: itemArea
        color: "blue"
        anchors.fill: parent

        Column {
            Row {
                spacing: 5
                Rectangle {
                    id: keyPressedDisplay
                    width: 154
                    height: 50
                    Text {
                        text: "Pressed"
                        anchors.centerIn: parent
                    }
                }
                Rectangle {
                    width: 155
                    height: 50
                    Text {
                        id: keyNumberDisplay
                        text: "0"
                        anchors.centerIn: parent
                    }
                }
                Rectangle {
                    id: keyReleasedDisplay
                    width: 154
                    height: 50
                    Text {
                        text: "Released"
                        anchors.centerIn: parent
                    }
                }
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
