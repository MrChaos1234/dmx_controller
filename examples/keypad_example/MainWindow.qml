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
