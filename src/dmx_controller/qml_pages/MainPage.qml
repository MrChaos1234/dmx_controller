import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_components"

Item {
    id: mainPaige
    anchors.fill: parent
    Rectangle {
        id: s
        anchors.fill: parent
        color: "#121212"

        Text {
            id: text
            anchors.centerIn: parent
            text: "Main Page Placeholder"
            font.pixelSize: 30
            color: "#ffffff"
        }
    }
}

