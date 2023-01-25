import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Window {
    visible: true
    visibility: Window.FullScreen

    Item {
        id: root

        StageView {
            id: stageView
            anchors.left: parent.left
            anchors.top: parent.top
            qml_presentation_model: stageViewQmlPresentationModel
        }
    }

}
