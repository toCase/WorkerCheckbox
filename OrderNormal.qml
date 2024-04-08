import QtQuick 6.5
import QtQuick.Controls 6.5
import QtQuick.Controls.Fusion
import QtQuick.Layouts

Item {

    function load() {
        modelOrderN.loadModel()
    }

    QtObject {
        id: internal

        function makeSell(){
            timerOff()
            tOrders.data_setter(1)
            tOrders.start()
        }
    }

    Connections {
        target: tOrders
        function onStarted(){
            progressBar.visible = true
            progressBar.value = 0
            but_load.enabled = false
        }
        function onWorking(val){
            progressBar.value = val
            // modelOrderN.loadModel()
        }
        function onFinished(){
            progressBar.visible = false
            progressBar.value = 0
            but_load.enabled = true
            modelOrderN.loadModel()
        }
        function onFail(message){
            progressBar.visible = false
            progressBar.value = 0
            but_load.enabled = true
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
            model: modelOrderN
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
                            visible: false
                            Layout.minimumWidth: 80
                            Layout.maximumWidth: 80
                            text: id
                        }
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
                        Label {
                            Layout.minimumWidth: 50
                            Layout.maximumWidth: 50
                            Layout.rightMargin: 50
                            font.pointSize: 11
                            font.bold: true
                            horizontalAlignment: Qt.AlignRight
                            verticalAlignment: Qt.AlignVCenter
                            color: clr
                            text: statusCB
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

        ProgressBar {
            id: progressBar

            Layout.fillWidth: true
            Layout.minimumHeight: 5
            Layout.maximumHeight: 5

            visible: false
            value: 0
        }

        Button {
            id: but_load
            Layout.fillWidth: true
            Layout.minimumHeight: 35
            Layout.maximumHeight: 35

            text: qsTr("Завантажити до Checkbox")

            onClicked: {
                internal.makeSell()
            }
        }

    }


}
