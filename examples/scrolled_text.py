""" Demo of how to use scrollbars on Text widget """
import tkinter as tk

import guitk as ui

sample_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ut ornare nunc. Duis vulputate sodales ultrices. Nulla vitae nisl at magna consequat semper ut vel mi. Proin dignissim efficitur nisi sed pulvinar. Interdum et malesuada fames ac ante ipsum primis in faucibus. Etiam pulvinar est tellus, nec rutrum purus aliquet sed. Vivamus non ornare tortor. Aenean sodales congue tincidunt. Aliquam ut mauris eget augue dictum scelerisque. Praesent in turpis a magna ullamcorper ultricies. Suspendisse efficitur ullamcorper turpis, at molestie lacus rhoncus id. Fusce faucibus sagittis molestie. Aenean et enim sollicitudin, bibendum odio vitae, mattis felis.

Donec quis justo in orci gravida condimentum. Vestibulum sagittis maximus ullamcorper. Quisque sit amet risus a nisl suscipit lobortis. Mauris luctus, mauris a viverra euismod, dolor neque volutpat massa, a maximus diam arcu a velit. Mauris magna ligula, aliquam nec sagittis id, commodo id turpis. Pellentesque et finibus metus, nec pretium leo. Duis ullamcorper sit amet metus ut fringilla. Cras tincidunt nisi eu consectetur suscipit. Duis rhoncus fringilla aliquam.

Cras risus sem, mollis quis consectetur congue, mattis facilisis nisl. Morbi vestibulum nunc non nunc mollis venenatis. Nullam massa ex, posuere id felis vel, tincidunt pellentesque sem. Donec id ante risus. Pellentesque id ipsum sodales, sollicitudin justo sit amet, lobortis lorem. Cras lorem nisl, congue nec magna non, ultrices malesuada nulla. Maecenas enim neque, ullamcorper eget libero eget, mollis malesuada nunc. Integer dignissim mauris nec iaculis consequat. Suspendisse lectus magna, aliquam vestibulum tristique id, volutpat id ipsum. Pellentesque ullamcorper quis nisi at molestie. Vestibulum eu arcu iaculis, fringilla orci vitae, pellentesque enim. Etiam accumsan felis nec nisi placerat, a commodo urna fringilla. Sed sit amet ex sed lectus tempus dapibus vel sit amet quam. In vel augue eu augue congue congue vel porttitor augue. Donec eu dolor id ligula tempor egestas non at nulla.

Cras ut felis a velit rutrum volutpat et auctor elit. Duis dapibus porta molestie. Sed a nisl sagittis, convallis eros nec, tincidunt est. Nulla vulputate risus at porta hendrerit. Etiam sodales pharetra mauris a pellentesque. Nunc cursus eu ipsum a porta. Sed blandit consequat arcu. Suspendisse vulputate nisi nec nulla consectetur, eget vehicula dui pulvinar. Proin vestibulum, leo id ullamcorper aliquam, magna massa laoreet lectus, lobortis faucibus ex risus at ipsum. Cras vitae ultricies purus, sed iaculis purus. Vestibulum lobortis finibus lectus, sed auctor enim ultricies cursus. Donec eleifend eros non felis mollis bibendum. Proin sed commodo purus. Donec blandit tincidunt iaculis. Duis scelerisque nibh tortor, a sagittis sapien fringilla non. Mauris rutrum tempus tortor, vel scelerisque elit viverra id.

Etiam vitae ex vulputate, tincidunt metus eu, mattis neque. In ex ligula, sodales a eros eget, volutpat cursus nunc. Ut ultricies quam eu rutrum ornare. Pellentesque elementum rutrum facilisis. Suspendisse vel tortor ante. Duis vehicula metus a commodo tempus. Praesent at velit ut est dapibus maximus. Aliquam mauris orci, aliquet sed molestie eget, venenatis eu mi. Mauris et mauris nec nisl venenatis condimentum. Phasellus vitae nisi sed enim porttitor tempus. Curabitur consectetur placerat est viverra euismod. Quisque dapibus dignissim metus, a congue lacus cursus in. Aliquam ut mi tortor.

In mattis tincidunt massa, sit amet luctus ligula congue vel. Sed magna augue, blandit vitae mollis eget, imperdiet in nibh. Aenean sapien metus, rutrum ac aliquam et, ultrices eget lorem. Morbi vitae ligula ac nisl mollis cursus a eu sem. Quisque fringilla eros non lacus congue pulvinar. Morbi quis consectetur ligula, at ultricies nulla. Ut non dui ultrices, imperdiet urna id, semper nunc. In rhoncus augue quis venenatis facilisis. Aliquam elementum lectus tempor turpis venenatis bibendum at in nunc. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mollis ligula non dui luctus, ac pulvinar justo facilisis. Duis volutpat mi nec massa sodales hendrerit. In sed convallis metus, vel feugiat orci. Vivamus non cursus nibh, eget tristique lectus.

Ut pulvinar semper mauris a finibus. Morbi a libero sapien. Etiam ut dolor magna. Vivamus maximus justo eu lacinia feugiat. Praesent feugiat lacinia erat. Nam feugiat at dui sit amet rutrum. Suspendisse maximus dui ligula, id cursus ligula gravida eget. Mauris venenatis mauris elementum tortor porttitor, non tempus nisi mollis. Sed egestas nisi nec diam suscipit elementum. Aliquam varius, metus ac auctor molestie, turpis nisi rhoncus dolor, nec elementum felis mauris eget est. Sed ac turpis et lectus hendrerit rhoncus.

Etiam ut luctus mi, eget dignissim velit. Maecenas eleifend ultricies placerat. In in porta nisi. Duis aliquet eleifend nisi, nec porttitor est viverra vel. Fusce eget mauris arcu. Donec molestie libero justo, eu maximus felis vulputate ut. In hac habitasse platea dictumst. Donec ligula justo, luctus sed maximus at, venenatis vitae mi. Donec quis tincidunt turpis. In ullamcorper orci ex, sit amet pharetra nibh imperdiet sed. Cras odio mi, dapibus vel turpis in, dictum bibendum mi. Suspendisse mi arcu, malesuada a scelerisque eget, lobortis quis lacus. Maecenas congue varius enim non ultrices.

Donec eu elit tempus, rhoncus dui vel, blandit nibh. Aliquam at sollicitudin erat, in condimentum eros. Nulla blandit ipsum at dui gravida tincidunt. Nulla enim mauris, tempor finibus aliquam sed, rhoncus ut turpis. Nulla odio purus, bibendum eu varius sed, ultrices in nisl. Aliquam volutpat eleifend felis, et efficitur magna maximus quis. Pellentesque tempus leo vel suscipit suscipit. Nunc sed justo tincidunt, fringilla massa ac, mollis enim. Mauris sodales vestibulum mauris, ac tempor leo. Phasellus mauris arcu, convallis et enim quis, scelerisque imperdiet ipsum. Quisque vel interdum nulla, sit amet hendrerit lectus. Fusce eu auctor massa. Maecenas id tellus convallis augue varius volutpat. Morbi convallis ipsum eget diam sodales viverra. Sed augue nulla, mollis non finibus id, consequat auctor magna.

Maecenas sem tortor, volutpat vel tortor egestas, condimentum luctus eros. Maecenas molestie velit orci, quis mollis nisl tincidunt at. Mauris accumsan est sit amet ligula porttitor dignissim. Ut hendrerit feugiat ex, eu auctor leo convallis sed. Sed volutpat ullamcorper aliquam. Fusce odio dui, volutpat volutpat commodo et, vehicula id ligula. Maecenas hendrerit est sit amet metus facilisis aliquet. Suspendisse vel massa velit. Nam at risus nibh. Sed tincidunt porta est, eu lacinia ex. Aenean ornare neque id felis porttitor faucibus. Nunc posuere pulvinar ligula. Donec fermentum ac massa quis consequat.

Vestibulum suscipit, turpis vel dictum commodo, ligula mauris malesuada augue, vulputate interdum metus sem sit amet tortor. Suspendisse ut enim finibus nibh pulvinar malesuada. Nam viverra dolor erat, ac commodo ipsum lobortis et. Nullam hendrerit ullamcorper nibh nec iaculis. Nullam rutrum, leo id sagittis pellentesque, lacus risus pulvinar ligula, sit amet cursus ligula lectus eu mi. Nulla cursus, dolor vitae blandit aliquet, tortor lacus tincidunt turpis, eu pharetra mi lorem a metus. Donec mattis dui ac dui bibendum, non consequat velit tincidunt. Aliquam id metus mattis massa dictum rhoncus rutrum in mi.

Nunc scelerisque vitae neque et varius. Proin tortor tortor, volutpat a vehicula a, faucibus vel tortor. Vivamus sollicitudin mi ipsum, quis semper leo rhoncus vitae. Etiam suscipit pulvinar sapien vitae efficitur. Morbi posuere tortor venenatis nulla elementum convallis. Sed viverra eros sapien, eu venenatis arcu viverra sed. Vivamus auctor, tortor sit amet mollis posuere, enim enim molestie mauris, nec tristique justo quam nec dolor. Quisque eget dolor gravida justo eleifend iaculis non pulvinar est. Vestibulum eget tellus et elit lacinia imperdiet. Pellentesque at sagittis nisl, vel lobortis arcu. Duis pellentesque nec ante vel ultricies. Vestibulum eget dictum dui, vel tincidunt odio. Nulla ac turpis id tortor posuere euismod vitae accumsan metus.

Vivamus elementum nisi vitae purus elementum ultrices. Praesent eget orci a tortor convallis egestas. Proin egestas ullamcorper tortor eu auctor. Phasellus ipsum diam, euismod quis nulla ac, porta congue nisi. Curabitur posuere, odio eu sollicitudin dictum, tortor justo tempus nisi, dapibus ultricies diam ante non mi. Aliquam varius, justo eget congue accumsan, turpis lorem egestas magna, a pellentesque ante mauris id turpis. Nam vel dictum felis, a auctor nisi. Proin consequat accumsan dui sit amet varius. Vestibulum finibus eros libero, vel suscipit velit dictum sit amet. Pellentesque ac ante non lorem finibus mollis. Pellentesque quis pretium lacus.

Vestibulum arcu arcu, accumsan accumsan neque sit amet, mattis finibus lacus. Sed commodo magna nec augue cursus, at pulvinar enim rutrum. Aliquam ornare nisi id sapien facilisis varius. In quis lectus eget lorem tristique placerat id et diam. Integer eu neque eget ipsum interdum elementum vel eu massa. Morbi cursus in mauris eget facilisis. Nullam fermentum, sapien id fermentum pretium, ipsum quam vehicula purus, eu commodo justo ex hendrerit libero. Vivamus viverra quis odio sit amet ultricies. Nulla non tortor est. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nullam id leo justo. Vestibulum faucibus massa nec ullamcorper gravida. Quisque mollis rutrum interdum. Cras tincidunt tempor orci ut varius. Fusce nec fermentum nibh.

Proin eget urna neque. Etiam a quam nec dui volutpat molestie vel non erat. Sed ac commodo dolor. Sed rhoncus arcu elit. Nam ut mauris aliquam, lobortis justo eu, lobortis sapien. Praesent dolor ipsum, commodo a congue id, consectetur et augue. Donec eget dui non lacus pulvinar mattis.

Nulla sed imperdiet augue. Sed eu commodo est. Praesent vestibulum nisi ipsum, id euismod orci tempus nec. Proin viverra fringilla molestie. Integer ut nunc lacus. Proin sit amet euismod leo. Morbi at dolor ac ex ultricies accumsan a vel ante.

Phasellus suscipit, orci ut porta mattis, mi mi vehicula leo, vitae facilisis ex sem vel erat. Suspendisse nibh orci, vestibulum quis mi eu, suscipit elementum ante. Nulla mollis quis velit non faucibus. Fusce vel ligula ac lacus malesuada euismod eu vitae metus. Aliquam massa sem, sagittis et tempus eu, semper id risus. Cras accumsan commodo orci, ac rutrum felis porta a. Quisque pellentesque ornare laoreet. Curabitur pellentesque, nunc mattis iaculis fringilla, felis risus consectetur leo, in volutpat tellus magna mattis ipsum. Aliquam quis fermentum eros. Vestibulum quis viverra tellus. Aenean accumsan nunc id tellus sodales tristique.

Ut malesuada lectus vel risus maximus lobortis. Maecenas ac ante erat. Sed velit mauris, scelerisque et nisl id, ultrices molestie lectus. Phasellus at blandit tortor. Vivamus bibendum urna sed volutpat malesuada. Aenean consequat congue dui, ut ullamcorper diam hendrerit ut. Mauris leo odio, commodo vitae nisl at, accumsan malesuada odio. Phasellus libero orci, placerat vitae accumsan et, pharetra non sapien. Vivamus condimentum malesuada sapien, ac sagittis nisi fermentum et. Ut varius, ante et luctus placerat, dui dui dignissim libero, non vestibulum mi magna et nunc. Morbi sed risus at arcu gravida venenatis consectetur vel odio. Proin a est non ante ultricies mollis.

Suspendisse aliquam dui a libero luctus placerat. Quisque tempus imperdiet tortor, a aliquam arcu porttitor a. In congue metus sed consectetur facilisis. Mauris ac sem ante. Quisque hendrerit, turpis eget viverra semper, lorem velit tempor urna, a ullamcorper dolor tortor vitae arcu. Ut gravida mattis neque ac lacinia. Etiam venenatis sed arcu vel suscipit. Quisque eleifend metus mauris, et pretium justo malesuada nec. Suspendisse potenti. Donec et massa lectus. Nam et odio neque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras congue, quam sit amet auctor tempus, eros eros blandit dolor, sit amet finibus risus mi nec dolor.

Pellentesque maximus turpis est. Quisque nec sapien sed leo dignissim malesuada non varius arcu. Ut tristique turpis id ipsum elementum placerat et at risus. Praesent hendrerit dictum lacinia. Aenean dictum velit vehicula malesuada venenatis. In ultricies vestibulum purus. Nulla et leo eu nunc sagittis placerat nec facilisis augue. Donec vestibulum, metus ac viverra euismod, erat velit dapibus nibh, eu interdum turpis justo at ligula.
"""

sample_text = "\n".join(
    str(idx) + " " + line for idx, line in enumerate(sample_text.splitlines())
)


class ScrollDemo(ui.Window):
    def config(self):
        self.title = "Scroll Demo"

        with ui.VLayout():
            with ui.HStack():
                with ui.VStack():
                    ui.Label("No Scrollbar")
                    ui.Text(
                        key="TEXT_NO_SCROLL",
                        text=sample_text,
                        width=40,
                        height=20,
                        wrap=tk.NONE,
                    )
                with ui.VStack():
                    ui.Label("Vertical/Horizontal Scrollbars")
                    ui.Text(
                        key="TEXT_VH_SCROLL",
                        vscrollbar=True,
                        hscrollbar=True,
                        text=sample_text,
                        width=40,
                        height=20,
                        wrap=tk.NONE,
                    )
            with ui.HStack():
                with ui.VStack():
                    ui.Label("Horizontal Scrollbar")
                    ui.Text(
                        key="TEXT_H_SCROLL",
                        hscrollbar=True,
                        text=sample_text,
                        width=40,
                        height=20,
                        wrap=tk.NONE,
                    )
                with ui.VStack():
                    ui.Label("Vertical Scrollbar")
                    ui.Text(
                        key="TEXT_V_SCROLL",
                        vscrollbar=True,
                        text=sample_text,
                        width=40,
                        height=20,
                        wrap=tk.NONE,
                    )


if __name__ == "__main__":
    ScrollDemo().run()
