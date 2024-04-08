import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Controls.Fusion
import QtQuick.Layouts

Item {


    function load(){
        modelOrderT.loadModel()
    }

    QtObject {
        id: internal

        function makeTTN(){
            timerOff()
            modelOrderT.makeOrders()
        }
    }

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        spacing: 10

        ListView {
            id: table
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: modelOrderT
            clip: true
            delegate: Item {

                width: table.width
                implicitHeight: itemCol.implicitHeight

                ColumnLayout{
                    id: itemCol
                    anchors.fill: parent

                    RowLayout {
                        Layout.fillWidth: true
                        Layout.minimumHeight: 35
                        Layout.maximumHeight: 35
                        spacing: 10

                        Label {
                            Layout.minimumWidth: 60
                            Layout.maximumWidth: 60
                            text: num
                            font.pointSize: 11
                            font.bold: true
                            horizontalAlignment: Qt.AlignLeft
                            verticalAlignment: Qt.AlignVCenter
                        }

                        Label {
                            Layout.fillWidth:true
                            text: phone
                            font.pointSize: 11
                            font.bold: true
                            horizontalAlignment: Qt.AlignLeft
                            verticalAlignment: Qt.AlignVCenter

                        }
                        Label {
                            Layout.minimumWidth: 200
                            Layout.maximumWidth: 200
                            Layout.rightMargin: 50
                            text: ttn
                            font.pointSize: 11
                            font.bold: true
                            horizontalAlignment: Qt.AlignRight
                            verticalAlignment: Qt.AlignVCenter
                        }
                    }

                    Repeater {
                        Layout.fillWidth: true
                        implicitHeight: detailEl.implicitHeight
                        model: base.detail_getX(id)

                        Text {
                            id: detailEl
                            leftPadding: 50
                            height: 20

                            required property string modelData
                            text: modelData
                            font.pointSize: 9
                            font.italic: true
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.minimumHeight: 3
                        Layout.maximumHeight: 3

                        color: "#660066"
                    }
                }
            }
        }
        Button {
            id: but_load
            Layout.fillWidth: true
            Layout.minimumHeight: 35
            Layout.maximumHeight: 35

            text: qsTr("Завантажити до ТТН")
            onClicked: {
                internal.makeTTN()
            }
        }

    }
}
