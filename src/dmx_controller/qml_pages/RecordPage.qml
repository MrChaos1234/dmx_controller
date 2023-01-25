import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_components"

Item {
    id: recordPage
    anchors.fill: parent
    Rectangle {
        id: s
        anchors.fill: parent
        color: "#121212"

        Text {
            id: text
            anchors.centerIn: parent
            text: "Record Page Placeholder"
            font.pixelSize: 30
            color: "#ffffff"
        }
    }
}

