import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_components"

Item {
    id: setupPage
    anchors.fill: parent
    Rectangle {
        id: s
        anchors.fill: parent
        color: "#121212"

        Text {
            id: text
            anchors.centerIn: parent
            text: "Setup Page Placeholder"
            font.pixelSize: 30
            color: "#ffffff"
        }

        DmxFixturePatch {
            id: dmxFixturePatchView
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.top: parent.top
        }

        Rectangle {
            color: "#1b1b1b"
            anchors.left: dmxFixturePatchView.right
            width: 1100
            height: 800
            border.color: "orange"
            border.width: 4

            Text {
                id: text2
                anchors.centerIn: parent
                text: "Stage View Placeholder"
                font.pixelSize: 30
                color: "#ffffff"
            }

        }
    }
}

