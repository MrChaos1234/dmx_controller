import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "../qml_components"

Item {
    id: livePage
    anchors.fill: parent
    Rectangle {
        id: livePageRect
        anchors.fill: parent
        color: "#121212"

        ButtonGridView {
            id: buttonGridView
            anchors.left: parent.left
            anchors.top: parent.top
        }

        CueList {
            id: cueList
            anchors.left: parent.left
            anchors.leftMargin: 1060
            anchors.top: parent.top
            height: 500
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 200
            show_only: true
        }

        EffectSetup {
            id: effectSetup
            anchors.left: parent.left
            anchors.leftMargin: 1060
            anchors.top: cueList.bottom
            anchors.topMargin: 10
            anchors.bottom: parent.bottom
        }

    }
}

