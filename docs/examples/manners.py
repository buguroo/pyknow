from pyknow import *
from pyknow import watchers


class Guest(Fact):
    pass


class LastSeat(Fact):
    pass


class Seating(Fact):
    pass


class Context(Fact):
    pass


class Path(Fact):
    pass


class Chosen(Fact):
    pass


class Count(Fact):
    pass


class Manners(KnowledgeEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Rule('f1' << Context(state='start'),
          Guest(name='n' << W()),
          'f3' << Count(c='c' << W()))
    def assign_first_seat(self, f1, f3, n, c):
        self.declare(Seating(seat1=1,
                             name1=n,
                             name2=n,
                             seat2=1,
                             id=c,
                             pid=0,
                             path_done=True))

        self.declare(Path(id=c, name=n, seat=1))
        self.modify(f3, c=c + 1)
        print("seat 1", n, n, 1, c, 0, 1)
        self.modify(f1, state="assign_seats")


    @Rule('f1' << Context(state='assign_seats'),
          Seating(seat1='seat1' << W(),
                  seat2='seat2' << W(),
                  name2='n2' << W(),
                  id='id' << W(),
                  pid='pid' << W(),
                  path_done=True),
          Guest(name='n2' << W(), sex='s1' << W(), hobby='h1' << W()),
          Guest(name='g2' << W(), sex=~('s1' << W()), hobby='h1' << W()),
          'f5' << Count(c='c' << W()),
          ~Path(id='id' << W(), name='g2' << W()),
          ~Chosen(id='id' << W(), name='g2' << W(), hobby='h1' << W()))
    def find_seating(self, f1, seat1, seat2, n2, id, pid, s1, h1, g2, c, f5):
        self.declare(Seating(seat1=seat2, name1=n2, name2=g2, seat2=seat2+1,
                             id=c, pid=id, path_done=False))
        self.declare(Path(id=c, name=g2, seat=seat2+1))
        self.declare(Chosen(id=id, name=g2, hobby=h1))
        self.modify(f5, c=c + 1)

        print("seat", seat2, n2, g2)

        self.modify(f1, state="make_path")

    @Rule(Context(state="make_path"),
          Seating(id='id' << W(), pid='pid' << W(), path_done=False),
          Path(id='pid' << W(), name='n1' << W(), seat='s' << W()),
          ~Path(id='id' << W(), name='n1' << W()))
    def make_path(self, id, pid, n1, s):
        self.declare(Path(id=id, name=n1, seat=s))


    @Rule('f1' << Context(state="make_path"),
          'f2' << Seating(path_done=False))
    def path_done(self, f1, f2):
        self.modify(f2, path_done=True)
        self.modify(f1, state="check_done")

    @Rule('f1' << Context(state="check_done"),
          LastSeat(seat='l_seat' << W()),
          Seating(seat2='l_seat' << W()))
    def are_we_done(self, f1, l_seat):
        print("Yes, we are done!!")
        self.modify(f1, state="print_results")

    @Rule('f1' << Context(state="check_done"))
    def do_continue(self, f1):
        self.modify(f1, state="assign_seats")

    @Rule(Context(state="print_results"),
          Seating(id='id' << W(), seat2='s2' << W()),
          LastSeat(seat='s2' << W()),
          'f4' << Path(id='id' << W(), name='n' << W(), seat='s' << W()))
    def print_results(self, id, s2, f4, n, s):
        self.retract(f4)
        print(n, s)

    @Rule(Context(state="print_results"))
    def all_done(self):
        self.halt()


k = Manners()

## Manners 8
# k.deffacts(Guest(name="n1", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n1", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n2", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n2", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n3", sex="m", hobby="h1"))
# k.deffacts(Guest(name="n3", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n3", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n4", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n4", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n5", sex="f", hobby="h1"))
# k.deffacts(Guest(name="n5", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n5", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n6", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n6", sex="f", hobby="h1"))
# k.deffacts(Guest(name="n6", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n7", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n7", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n8", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n8", sex="m", hobby="h1"))
# k.deffacts(LastSeat(seat=8))


## Manners 16
# k.deffacts(Guest(name="n1", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n1", sex="f", hobby="h1"))
# k.deffacts(Guest(name="n1", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n2", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n2", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n3", sex="m", hobby="h1"))
# k.deffacts(Guest(name="n3", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n4", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n4", sex="m", hobby="h1"))
# k.deffacts(Guest(name="n5", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n5", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n6", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n6", sex="m", hobby="h1"))
# k.deffacts(Guest(name="n7", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n7", sex="f", hobby="h1"))
# k.deffacts(Guest(name="n7", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n8", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n8", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n9", sex="f", hobby="h1"))
# k.deffacts(Guest(name="n9", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n9", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n10", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n10", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n11", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n11", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n11", sex="m", hobby="h1"))
# k.deffacts(Guest(name="n12", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n12", sex="m", hobby="h1"))
# k.deffacts(Guest(name="n13", sex="m", hobby="h2"))
# k.deffacts(Guest(name="n13", sex="m", hobby="h3"))
# k.deffacts(Guest(name="n13", sex="m", hobby="h1"))
# k.deffacts(Guest(name="n14", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n14", sex="f", hobby="h1"))
# k.deffacts(Guest(name="n15", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n15", sex="f", hobby="h1"))
# k.deffacts(Guest(name="n15", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n16", sex="f", hobby="h3"))
# k.deffacts(Guest(name="n16", sex="f", hobby="h2"))
# k.deffacts(Guest(name="n16", sex="f", hobby="h1"))
# k.deffacts(LastSeat(seat=16))


## Manners 32
k.deffacts(Guest(name="n1", sex="m", hobby="h1"))
k.deffacts(Guest(name="n1", sex="m", hobby="h3"))
k.deffacts(Guest(name="n2", sex="f", hobby="h3"))
k.deffacts(Guest(name="n2", sex="f", hobby="h2"))
k.deffacts(Guest(name="n2", sex="f", hobby="h1"))
k.deffacts(Guest(name="n3", sex="f", hobby="h1"))
k.deffacts(Guest(name="n3", sex="f", hobby="h2"))
k.deffacts(Guest(name="n4", sex="f", hobby="h3"))
k.deffacts(Guest(name="n4", sex="f", hobby="h1"))
k.deffacts(Guest(name="n5", sex="f", hobby="h1"))
k.deffacts(Guest(name="n5", sex="f", hobby="h2"))
k.deffacts(Guest(name="n6", sex="m", hobby="h1"))
k.deffacts(Guest(name="n6", sex="m", hobby="h2"))
k.deffacts(Guest(name="n6", sex="m", hobby="h3"))
k.deffacts(Guest(name="n7", sex="f", hobby="h2"))
k.deffacts(Guest(name="n7", sex="f", hobby="h1"))
k.deffacts(Guest(name="n7", sex="f", hobby="h3"))
k.deffacts(Guest(name="n8", sex="f", hobby="h1"))
k.deffacts(Guest(name="n8", sex="f", hobby="h3"))
k.deffacts(Guest(name="n8", sex="f", hobby="h2"))
k.deffacts(Guest(name="n9", sex="f", hobby="h1"))
k.deffacts(Guest(name="n9", sex="f", hobby="h3"))
k.deffacts(Guest(name="n9", sex="f", hobby="h2"))
k.deffacts(Guest(name="n10", sex="m", hobby="h2"))
k.deffacts(Guest(name="n10", sex="m", hobby="h1"))
k.deffacts(Guest(name="n11", sex="m", hobby="h2"))
k.deffacts(Guest(name="n11", sex="m", hobby="h1"))
k.deffacts(Guest(name="n12", sex="m", hobby="h3"))
k.deffacts(Guest(name="n12", sex="m", hobby="h2"))
k.deffacts(Guest(name="n13", sex="m", hobby="h1"))
k.deffacts(Guest(name="n13", sex="m", hobby="h3"))
k.deffacts(Guest(name="n14", sex="m", hobby="h3"))
k.deffacts(Guest(name="n14", sex="m", hobby="h2"))
k.deffacts(Guest(name="n15", sex="f", hobby="h2"))
k.deffacts(Guest(name="n15", sex="f", hobby="h1"))
k.deffacts(Guest(name="n15", sex="f", hobby="h3"))
k.deffacts(Guest(name="n16", sex="f", hobby="h3"))
k.deffacts(Guest(name="n16", sex="f", hobby="h2"))
k.deffacts(Guest(name="n16", sex="f", hobby="h1"))
k.deffacts(Guest(name="n17", sex="m", hobby="h3"))
k.deffacts(Guest(name="n17", sex="m", hobby="h2"))
k.deffacts(Guest(name="n18", sex="f", hobby="h2"))
k.deffacts(Guest(name="n18", sex="f", hobby="h1"))
k.deffacts(Guest(name="n19", sex="f", hobby="h1"))
k.deffacts(Guest(name="n19", sex="f", hobby="h2"))
k.deffacts(Guest(name="n19", sex="f", hobby="h3"))
k.deffacts(Guest(name="n20", sex="f", hobby="h1"))
k.deffacts(Guest(name="n20", sex="f", hobby="h2"))
k.deffacts(Guest(name="n20", sex="f", hobby="h3"))
k.deffacts(Guest(name="n21", sex="m", hobby="h2"))
k.deffacts(Guest(name="n21", sex="m", hobby="h3"))
k.deffacts(Guest(name="n21", sex="m", hobby="h1"))
k.deffacts(Guest(name="n22", sex="f", hobby="h1"))
k.deffacts(Guest(name="n22", sex="f", hobby="h2"))
k.deffacts(Guest(name="n22", sex="f", hobby="h3"))
k.deffacts(Guest(name="n23", sex="f", hobby="h3"))
k.deffacts(Guest(name="n23", sex="f", hobby="h1"))
k.deffacts(Guest(name="n23", sex="f", hobby="h2"))
k.deffacts(Guest(name="n24", sex="m", hobby="h1"))
k.deffacts(Guest(name="n24", sex="m", hobby="h3"))
k.deffacts(Guest(name="n25", sex="f", hobby="h3"))
k.deffacts(Guest(name="n25", sex="f", hobby="h2"))
k.deffacts(Guest(name="n25", sex="f", hobby="h1"))
k.deffacts(Guest(name="n26", sex="f", hobby="h3"))
k.deffacts(Guest(name="n26", sex="f", hobby="h2"))
k.deffacts(Guest(name="n26", sex="f", hobby="h1"))
k.deffacts(Guest(name="n27", sex="m", hobby="h3"))
k.deffacts(Guest(name="n27", sex="m", hobby="h1"))
k.deffacts(Guest(name="n27", sex="m", hobby="h2"))
k.deffacts(Guest(name="n28", sex="m", hobby="h3"))
k.deffacts(Guest(name="n28", sex="m", hobby="h1"))
k.deffacts(Guest(name="n29", sex="m", hobby="h3"))
k.deffacts(Guest(name="n29", sex="m", hobby="h2"))
k.deffacts(Guest(name="n29", sex="m", hobby="h1"))
k.deffacts(Guest(name="n30", sex="m", hobby="h2"))
k.deffacts(Guest(name="n30", sex="m", hobby="h1"))
k.deffacts(Guest(name="n30", sex="m", hobby="h3"))
k.deffacts(Guest(name="n31", sex="m", hobby="h2"))
k.deffacts(Guest(name="n31", sex="m", hobby="h1"))
k.deffacts(Guest(name="n32", sex="m", hobby="h1"))
k.deffacts(Guest(name="n32", sex="m", hobby="h3"))
k.deffacts(Guest(name="n32", sex="m", hobby="h2"))
k.deffacts(LastSeat(seat=32))


## Manners 64
# k.deffacts(Guest(name=1, sex="m", hobby="h2"))
# k.deffacts(Guest(name=1, sex="m", hobby="h1"))
# k.deffacts(Guest(name=1, sex="m", hobby="h3"))
# k.deffacts(Guest(name=2, sex="f", hobby="h2"))
# k.deffacts(Guest(name=2, sex="f", hobby="h1"))
# k.deffacts(Guest(name=2, sex="f", hobby="h3"))
# k.deffacts(Guest(name=3, sex="m", hobby="h3"))
# k.deffacts(Guest(name=3, sex="m", hobby="h2"))
# k.deffacts(Guest(name=4, sex="m", hobby="h3"))
# k.deffacts(Guest(name=4, sex="m", hobby="h2"))
# k.deffacts(Guest(name=4, sex="m", hobby="h1"))
# k.deffacts(Guest(name=5, sex="m", hobby="h2"))
# k.deffacts(Guest(name=5, sex="m", hobby="h1"))
# k.deffacts(Guest(name=5, sex="m", hobby="h3"))
# k.deffacts(Guest(name=6, sex="m", hobby="h2"))
# k.deffacts(Guest(name=6, sex="m", hobby="h3"))
# k.deffacts(Guest(name=6, sex="m", hobby="h1"))
# k.deffacts(Guest(name=7, sex="f", hobby="h1"))
# k.deffacts(Guest(name=7, sex="f", hobby="h2"))
# k.deffacts(Guest(name=7, sex="f", hobby="h3"))
# k.deffacts(Guest(name=8, sex="m", hobby="h3"))
# k.deffacts(Guest(name=8, sex="m", hobby="h1"))
# k.deffacts(Guest(name=9, sex="m", hobby="h2"))
# k.deffacts(Guest(name=9, sex="m", hobby="h3"))
# k.deffacts(Guest(name=9, sex="m", hobby="h1"))
# k.deffacts(Guest(name=10, sex="m", hobby="h3"))
# k.deffacts(Guest(name=10, sex="m", hobby="h2"))
# k.deffacts(Guest(name=10, sex="m", hobby="h1"))
# k.deffacts(Guest(name=11, sex="m", hobby="h1"))
# k.deffacts(Guest(name=11, sex="m", hobby="h3"))
# k.deffacts(Guest(name=11, sex="m", hobby="h2"))
# k.deffacts(Guest(name=12, sex="f", hobby="h3"))
# k.deffacts(Guest(name=12, sex="f", hobby="h1"))
# k.deffacts(Guest(name=12, sex="f", hobby="h2"))
# k.deffacts(Guest(name=13, sex="m", hobby="h2"))
# k.deffacts(Guest(name=13, sex="m", hobby="h3"))
# k.deffacts(Guest(name=14, sex="m", hobby="h1"))
# k.deffacts(Guest(name=14, sex="m", hobby="h2"))
# k.deffacts(Guest(name=15, sex="m", hobby="h2"))
# k.deffacts(Guest(name=15, sex="m", hobby="h3"))
# k.deffacts(Guest(name=15, sex="m", hobby="h1"))
# k.deffacts(Guest(name=16, sex="f", hobby="h2"))
# k.deffacts(Guest(name=16, sex="f", hobby="h3"))
# k.deffacts(Guest(name=17, sex="f", hobby="h3"))
# k.deffacts(Guest(name=17, sex="f", hobby="h2"))
# k.deffacts(Guest(name=18, sex="m", hobby="h1"))
# k.deffacts(Guest(name=18, sex="m", hobby="h3"))
# k.deffacts(Guest(name=18, sex="m", hobby="h2"))
# k.deffacts(Guest(name=19, sex="f", hobby="h3"))
# k.deffacts(Guest(name=19, sex="f", hobby="h1"))
# k.deffacts(Guest(name=20, sex="f", hobby="h1"))
# k.deffacts(Guest(name=20, sex="f", hobby="h3"))
# k.deffacts(Guest(name=20, sex="f", hobby="h2"))
# k.deffacts(Guest(name=21, sex="m", hobby="h2"))
# k.deffacts(Guest(name=21, sex="m", hobby="h3"))
# k.deffacts(Guest(name=22, sex="m", hobby="h2"))
# k.deffacts(Guest(name=22, sex="m", hobby="h3"))
# k.deffacts(Guest(name=23, sex="f", hobby="h1"))
# k.deffacts(Guest(name=23, sex="f", hobby="h2"))
# k.deffacts(Guest(name=24, sex="f", hobby="h3"))
# k.deffacts(Guest(name=24, sex="f", hobby="h1"))
# k.deffacts(Guest(name=24, sex="f", hobby="h2"))
# k.deffacts(Guest(name=25, sex="f", hobby="h3"))
# k.deffacts(Guest(name=25, sex="f", hobby="h1"))
# k.deffacts(Guest(name=25, sex="f", hobby="h2"))
# k.deffacts(Guest(name=26, sex="m", hobby="h2"))
# k.deffacts(Guest(name=26, sex="m", hobby="h1"))
# k.deffacts(Guest(name=26, sex="m", hobby="h3"))
# k.deffacts(Guest(name=27, sex="f", hobby="h2"))
# k.deffacts(Guest(name=27, sex="f", hobby="h3"))
# k.deffacts(Guest(name=27, sex="f", hobby="h1"))
# k.deffacts(Guest(name=28, sex="m", hobby="h1"))
# k.deffacts(Guest(name=28, sex="m", hobby="h2"))
# k.deffacts(Guest(name=29, sex="f", hobby="h2"))
# k.deffacts(Guest(name=29, sex="f", hobby="h3"))
# k.deffacts(Guest(name=29, sex="f", hobby="h1"))
# k.deffacts(Guest(name=30, sex="f", hobby="h2"))
# k.deffacts(Guest(name=30, sex="f", hobby="h1"))
# k.deffacts(Guest(name=30, sex="f", hobby="h3"))
# k.deffacts(Guest(name=31, sex="m", hobby="h1"))
# k.deffacts(Guest(name=31, sex="m", hobby="h2"))
# k.deffacts(Guest(name=31, sex="m", hobby="h3"))
# k.deffacts(Guest(name=32, sex="m", hobby="h1"))
# k.deffacts(Guest(name=32, sex="m", hobby="h2"))
# k.deffacts(Guest(name=33, sex="m", hobby="h2"))
# k.deffacts(Guest(name=33, sex="m", hobby="h3"))
# k.deffacts(Guest(name=33, sex="m", hobby="h1"))
# k.deffacts(Guest(name=34, sex="f", hobby="h2"))
# k.deffacts(Guest(name=34, sex="f", hobby="h1"))
# k.deffacts(Guest(name=34, sex="f", hobby="h3"))
# k.deffacts(Guest(name=35, sex="f", hobby="h2"))
# k.deffacts(Guest(name=35, sex="f", hobby="h3"))
# k.deffacts(Guest(name=36, sex="m", hobby="h2"))
# k.deffacts(Guest(name=36, sex="m", hobby="h1"))
# k.deffacts(Guest(name=37, sex="m", hobby="h2"))
# k.deffacts(Guest(name=37, sex="m", hobby="h1"))
# k.deffacts(Guest(name=38, sex="f", hobby="h1"))
# k.deffacts(Guest(name=38, sex="f", hobby="h3"))
# k.deffacts(Guest(name=38, sex="f", hobby="h2"))
# k.deffacts(Guest(name=39, sex="m", hobby="h3"))
# k.deffacts(Guest(name=39, sex="m", hobby="h1"))
# k.deffacts(Guest(name=39, sex="m", hobby="h2"))
# k.deffacts(Guest(name=40, sex="f", hobby="h1"))
# k.deffacts(Guest(name=40, sex="f", hobby="h2"))
# k.deffacts(Guest(name=40, sex="f", hobby="h3"))
# k.deffacts(Guest(name=41, sex="m", hobby="h2"))
# k.deffacts(Guest(name=41, sex="m", hobby="h1"))
# k.deffacts(Guest(name=41, sex="m", hobby="h3"))
# k.deffacts(Guest(name=42, sex="m", hobby="h3"))
# k.deffacts(Guest(name=42, sex="m", hobby="h1"))
# k.deffacts(Guest(name=43, sex="m", hobby="h1"))
# k.deffacts(Guest(name=43, sex="m", hobby="h3"))
# k.deffacts(Guest(name=43, sex="m", hobby="h2"))
# k.deffacts(Guest(name=44, sex="m", hobby="h3"))
# k.deffacts(Guest(name=44, sex="m", hobby="h1"))
# k.deffacts(Guest(name=44, sex="m", hobby="h2"))
# k.deffacts(Guest(name=45, sex="m", hobby="h1"))
# k.deffacts(Guest(name=45, sex="m", hobby="h2"))
# k.deffacts(Guest(name=46, sex="f", hobby="h1"))
# k.deffacts(Guest(name=46, sex="f", hobby="h2"))
# k.deffacts(Guest(name=46, sex="f", hobby="h3"))
# k.deffacts(Guest(name=47, sex="m", hobby="h1"))
# k.deffacts(Guest(name=47, sex="m", hobby="h2"))
# k.deffacts(Guest(name=48, sex="f", hobby="h3"))
# k.deffacts(Guest(name=48, sex="f", hobby="h2"))
# k.deffacts(Guest(name=49, sex="m", hobby="h3"))
# k.deffacts(Guest(name=49, sex="m", hobby="h2"))
# k.deffacts(Guest(name=50, sex="m", hobby="h2"))
# k.deffacts(Guest(name=50, sex="m", hobby="h3"))
# k.deffacts(Guest(name=51, sex="f", hobby="h2"))
# k.deffacts(Guest(name=51, sex="f", hobby="h1"))
# k.deffacts(Guest(name=51, sex="f", hobby="h3"))
# k.deffacts(Guest(name=52, sex="m", hobby="h1"))
# k.deffacts(Guest(name=52, sex="m", hobby="h2"))
# k.deffacts(Guest(name=52, sex="m", hobby="h3"))
# k.deffacts(Guest(name=53, sex="f", hobby="h2"))
# k.deffacts(Guest(name=53, sex="f", hobby="h1"))
# k.deffacts(Guest(name=54, sex="f", hobby="h1"))
# k.deffacts(Guest(name=54, sex="f", hobby="h2"))
# k.deffacts(Guest(name=54, sex="f", hobby="h3"))
# k.deffacts(Guest(name=55, sex="f", hobby="h1"))
# k.deffacts(Guest(name=55, sex="f", hobby="h2"))
# k.deffacts(Guest(name=55, sex="f", hobby="h3"))
# k.deffacts(Guest(name=56, sex="f", hobby="h2"))
# k.deffacts(Guest(name=56, sex="f", hobby="h1"))
# k.deffacts(Guest(name=56, sex="f", hobby="h3"))
# k.deffacts(Guest(name=57, sex="f", hobby="h3"))
# k.deffacts(Guest(name=57, sex="f", hobby="h2"))
# k.deffacts(Guest(name=57, sex="f", hobby="h1"))
# k.deffacts(Guest(name=58, sex="f", hobby="h3"))
# k.deffacts(Guest(name=58, sex="f", hobby="h1"))
# k.deffacts(Guest(name=58, sex="f", hobby="h2"))
# k.deffacts(Guest(name=59, sex="f", hobby="h1"))
# k.deffacts(Guest(name=59, sex="f", hobby="h2"))
# k.deffacts(Guest(name=59, sex="f", hobby="h3"))
# k.deffacts(Guest(name=60, sex="f", hobby="h3"))
# k.deffacts(Guest(name=60, sex="f", hobby="h1"))
# k.deffacts(Guest(name=61, sex="f", hobby="h3"))
# k.deffacts(Guest(name=61, sex="f", hobby="h2"))
# k.deffacts(Guest(name=62, sex="f", hobby="h1"))
# k.deffacts(Guest(name=62, sex="f", hobby="h2"))
# k.deffacts(Guest(name=62, sex="f", hobby="h3"))
# k.deffacts(Guest(name=63, sex="f", hobby="h3"))
# k.deffacts(Guest(name=63, sex="f", hobby="h1"))
# k.deffacts(Guest(name=63, sex="f", hobby="h2"))
# k.deffacts(Guest(name=64, sex="f", hobby="h3"))
# k.deffacts(Guest(name=64, sex="f", hobby="h2"))
# k.deffacts(LastSeat(seat=64))

k.deffacts(Count(c=1))
k.deffacts(Context(state="start"))

k.reset()
k.run()
