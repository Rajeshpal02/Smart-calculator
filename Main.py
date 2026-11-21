from pyscript import document, when
from pyodide.ffi import create_proxy

mode = None
display = document.querySelector("#display")
arithmetics = document.querySelector("#arithmetics")
operation = document.querySelector("#operation")
multidisplay = document.querySelector(".multidisplay")

display2 = None
display3 = None
display4 = None 
display5 = None
display6 = None 
display7 = None
display8 = None 
display9 = None
display10 = None
display11 = None
display12 = None
display13 = None
display14 = None
display15 = None

active_display = display


def set_active_display(event):
    global active_display
    active_display = event.target


display.addEventListener("focus", create_proxy(set_active_display))


@when("click", "#addition,#multiplication,#subtraction,#division,#modulus")
def operation_input(event):
    start = active_display.selectionStart or len(active_display.value)
    end = active_display.selectionEnd or len(active_display.value)
    value = active_display.value
    operator = event.target.innerText

    active_display.value = value[:start] + operator + value[end:]
    position = start + len(operator)
    active_display.focus()
    active_display.setSelectionRange(position, position)


def select_category(selected):
    global active_display, mode
    categories = ["arithmetics", "logical", "binary", "mensuration"]
    for category in categories:
        button = document.querySelector("#" + category)
        if button:
            if category == selected:
                button.classList.add("selected")
            else:
                button.classList.remove("selected")
    
    
    active_display = display
    mode = None


select_category("arithmetics")



@when("click", "#num0,#num1,#num2,#num3,#num4,#num5,#num6,#num7,#num8,#num9,#num00,#point")
def number_input(event):
    number = event.target.innerText
    
    
    start = active_display.selectionStart if active_display.selectionStart is not None else len(active_display.value)
    end = active_display.selectionEnd if active_display.selectionEnd is not None else len(active_display.value)

    value = active_display.value
    active_display.value = value[:start] + number + value[end:]

    position = start + len(number)
    active_display.focus()
    active_display.setSelectionRange(position, position)


@when("click", "#delete")
def delete(event):
    active_display.value = active_display.value[:-1]


@when("click", "#allclear")
def allclear(event):
    display.value = ""
    if display2:
        display2.value = ""
    if display3:
        display3.value = ""
    if display4:
        display4.value = ""
    if display5:
        display5.value = ""


@when("click", "#bracket")
def bracket(event):
    start = active_display.selectionStart or len(active_display.value)
    end = active_display.selectionEnd or len(active_display.value)
    value = active_display.value

    active_display.value = value[:start] + "()" + value[end:]
    active_display.focus()
    active_display.setSelectionRange(start + 1, start + 1)


@when("click", "#arithmetics")
def arithematics(event):
    select_category("arithmetics")
    multidisplay.innerHTML = ""
    operation.innerHTML = """
    <div class="oprow">
     <button id="addition">+</button>
     <button id="subtraction">-</button>
     <button id="multiplication">*</button>
     <button id="division">/</button>
     <button id="modulus">%</button>
    </div>
    """
    @when("click", ".oprow button")
    def operation_new(event):
        operation_input(event)


@when("click", "#logical")
def logical(event):
    select_category("logical")
    multidisplay.innerHTML = ""
    operation.innerHTML = """
    <div class="oprow2">
     <button> and </button>
     <button> or </button>
     <button id="not"> not </button>
     <button id="xor"> xor </button>
     <button id="xnor"> xnor </button>
    </div>
    """
    @when("click", ".oprow2 button")
    def operation_click(event):
        display.value += " " + event.target.innerText + " "

    @when("click", "#not")
    def select_not(event):
        global mode
        mode = "not"

    @when("click", "#xor")
    def select_xor(event):
        global mode
        mode = "xor"

    @when("click", "#xnor")
    def select_xnor(event):
        global mode
        mode = "xnor"


def logical_xor():
    xor_expression = display.value.split("xor")
    first = bool(eval(xor_expression[0].strip()))
    second = bool(eval(xor_expression[1].strip()))
    display.value = str(first != second)


def logical_xnor():
    xnor_expression = display.value.split("xnor")
    first = bool(eval(xnor_expression[0].strip()))
    second = bool(eval(xnor_expression[1].strip()))
    display.value = str(first == second)


def logical_not():
    display.value = str(eval(display.value))


@when("click", "#binary")
def binary(event):
    select_category("binary")
    multidisplay.innerHTML = ""
    operation.innerHTML = """
    <p id="p1">Bitwise Operations</p>
    <div class="oprow3">
     <button>&</button>
     <button>|</button>
     <button>~</button>
     <button><<</button>
     <button>>></button>
    </div>
    <p id="p2">Binary Convertion and Arithmetics</p>
    <div class="oprow5">
     <button id="bindec">bin->dec</button>
     <button id="decbin">dec->bin</button>
     <button id="bin-add">bin(+)</button>
     <button id="bin-sub">bin(-)</button>
    </div>
    """
    @when("click", ".oprow3 button")
    def binay_new(event):
        display.value += " " + event.target.innerText + " "

    @when("click", "#bindec")
    def select_bin_dec(event):
        global mode
        mode = "bin_dec"

    @when("click", "#decbin")
    def select_dec_bin(event):
        global mode
        mode = "dec_bin"

    @when("click", "#bin-add")
    def select_binay_add(event):
        global mode
        mode = "bin_add"
        display.value += " + "

    @when("click", "#bin-sub")
    def select_binary_sub(event):
        global mode
        mode = "bin_sub"
        display.value += " - "


def bin_to_dec():
    display.value = str(int(display.value, 2))


def dec_to_bin():
    display.value = bin(int(display.value))[2:]


def binary_add():
    binary_expression = display.value.split("+")
    answer = sum(int(b.strip(), 2) for b in binary_expression)
    display.value = bin(answer)[2:]


def binary_subtraction():
    binary_sub_expression = display.value.split("-")
    answer = int(binary_sub_expression[0].strip(), 2)
    for b in binary_sub_expression[1:]:
        answer -= int(b.strip(), 2)

    if answer < 0:
        display.value = "-" + bin(abs(answer))[2:]
    else:
        display.value = bin(answer)[2:]


@when("click", "#mensuration")
def mensuration(event):
    select_category("mensuration")
    multidisplay.innerHTML = ""
    operation.innerHTML = """
    <div class="oprow4">
     <button id="dd">2D</button>
     <button id="ddd">3D</button>
    </div>
    <div id="opr_mensuration"></div>
    """
    opr_mensuration = document.querySelector("#opr_mensuration")

    @when("click", "#dd")
    def select_2d(event):
        opr_mensuration.innerHTML = """
        <div class="oprow6">
         <button id="area">Area</button>
         <button id="perimeter">Perimeter</button>
         <button id="circumference">Circumference</button>
        </div>
        <div id="dd_mensuration"></div>
        """
        dd_mensuration = document.querySelector("#dd_mensuration")

        @when("click", "#area")
        def select_area(event):
            dd_mensuration.innerHTML = """
            <p id="p1">Area's</p>
            <div class="oprow7">
             <button id="a_rectangle">Rectangle</button>
             <button id="a_square">Square</button>
            </div>
            <div class="oprow7">
             <button id="a_circle">Circle</button>
             <button id="a_triangle">Triangle</button>
            </div>
            """

            @when("click", "#a_rectangle")
            def make_multidisplay(event):
                global mode, display2, display3, active_display
                mode = "a_rectangle"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="length.." id="display2" readonly>
                 <input type="text" placeholder="breadth.." id="display3" readonly>
                </div>
                """
                display2 = document.querySelector("#display2")
                display3 = document.querySelector("#display3")

                
                active_display = display2
                display2.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display2.addEventListener("click", proxy_fn)
                display3.addEventListener("click", proxy_fn)
                display2.addEventListener("focus", proxy_fn)
                display3.addEventListener("focus", proxy_fn)

              
            @when("click", "#a_triangle")
            def make_multidisplay(event):
                global mode, display4, display5, active_display
                mode = "a_triangle"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="base.." id="display4" readonly>
                 <input type="text" placeholder="height.." id="display5" readonly>
                </div>
                """
                display4 = document.querySelector("#display4")
                display5 = document.querySelector("#display5")

                
                active_display = display4
                display4.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display4.addEventListener("click", proxy_fn)
                display5.addEventListener("click", proxy_fn)
                display4.addEventListener("focus", proxy_fn)
                display5.addEventListener("focus", proxy_fn)

            @when("click", "#a_square")
            def make_multidisplay(event):
                global mode, display6, active_display
                mode = "a_square"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="Enter side of Square.." id="display6" readonly>
                </div>
                """
                display6 = document.querySelector("#display6")
                

                
                active_display = display6
                display6.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display6.addEventListener("click", proxy_fn)
                display6.addEventListener("focus", proxy_fn)

            @when("click", "#a_circle")
            def make_multidisplay(event):
                global mode, display7, active_display
                mode = "a_circle"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="Enter radius of circle.." id="display7" readonly>
                </div>
                """
                display7 = document.querySelector("#display7")
                

                
                active_display = display7
                display7.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display7.addEventListener("click", proxy_fn)
                display7.addEventListener("focus", proxy_fn)



        @when("click", "#perimeter")
        def select_perimerter(event):
            dd_mensuration.innerHTML = """
            <p id="p2">Perimeter's</p>
            <div class="oprow7">
             <button id="p_rectangle">Rectangle</button>
             <button id="p_square">Square</button>
            </div>
            <div class="oprow7">
             <button id="p_parallelogram">parallelogram</button>
             <button id="p_triangle">Triangle</button>
            </div>
            """
          
            @when("click", "#p_rectangle")
            def make_multidisplay(event):
                global mode,display8,display9, active_display
                mode = "p_rectangle"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="length..." id="display8" readonly>
                 <input type="text" placeholder="breadth..." id="display9" readonly>
                </div>
                """
                display8 = document.querySelector("#display8")
                display9 = document.querySelector("#display9")

                
                active_display = display8
                display8.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display8.addEventListener("click", proxy_fn)
                display9.addEventListener("click", proxy_fn)
                display8.addEventListener("focus", proxy_fn)
                display9.addEventListener("focus", proxy_fn)
              
            @when("click", "#p_square")
            def make_multidisplay(event):
                global mode, display10, active_display
                mode = "p_square"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="Enter side of Square.." id="display10" readonly>
                </div>
                """
                display10 = document.querySelector("#display10")
                

                
                active_display = display10
                display10.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display10.addEventListener("click", proxy_fn)
                display10.addEventListener("focus", proxy_fn)

              
            @when("click", "#p_parallelogram")
            def make_multidisplay(event):
                global mode,display8,display9, active_display
                mode = "p_rectangle"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="length..." id="display8" readonly>
                 <input type="text" placeholder="breadth..." id="display9" readonly>
                </div>
                """
                display8 = document.querySelector("#display8")
                display9 = document.querySelector("#display9")

                
                active_display = display8
                display8.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display8.addEventListener("click", proxy_fn)
                display9.addEventListener("click", proxy_fn)
                display8.addEventListener("focus", proxy_fn)
                display9.addEventListener("focus", proxy_fn)

            @when("click", "#p_triangle")
            def make_multidisplay(event):
                global mode, display12, display13, display14 ,active_display
                mode = "p_triangle"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="side(a).." id="display12" readonly>
                 <input type="text" placeholder="side(b).." id="display13" readonly>
                 <input type="text" placeholder="side(c).." id="display14" readonly>
                </div>
                """
                display12 = document.querySelector("#display12")
                display13 = document.querySelector("#display13")
                display14 = document.querySelector("#display14")

                
                active_display = display12
                display12.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display12.addEventListener("click", proxy_fn)
                display13.addEventListener("click", proxy_fn)
                display14.addEventListener("click", proxy_fn)
                display12.addEventListener("focus", proxy_fn)
                display13.addEventListener("focus", proxy_fn)
                display14.addEventListener("focus", proxy_fn)


        @when("click", "#circumference")
        def select_circumference(event):
            dd_mensuration.innerHTML = """
            <p id="p1">Circumference</p>
            <div class="oprow7">
              <button id="c_circle">circle</button>
            </div>
            """
            @when("click", "#c_circle")
            def make_multidisplay(event):
                global mode, display15, active_display
                mode = "c_circle"
                display.value = "" 

                multidisplay.innerHTML = """
                <div class="dualdisplay">
                 <input type="text" placeholder="Enter radius of circle.." id="display15" readonly>
                </div>
                """
                display15 = document.querySelector("#display15")
                

                
                active_display = display15
                display15.focus()

                
                proxy_fn = create_proxy(set_active_display)
                display15.addEventListener("click", proxy_fn)
                display15.addEventListener("focus", proxy_fn)

    @when("click", "#ddd")
    def select_3d(event):
      opr_mensuration.innerHTML = """
      <div class="oprow6">
       <button id="cube">cube□</button>
       <button id="cuboid">cuboid▱</button>
       <button id="cylinder">cylinder○</button>
      </div>
      <div class="oprow6">
       <button id="cone">cone▲</button>
       <button id="sphere">sphere●</button>
       <button id="hemisphere">hemisphere◒</button>
      </div>
      <div id="ddd_mensuration"></div>
      """
      ddd_mensuration=document.querySelector("#ddd_mensuration")
      @when("click","#cube")
      def select_cube(event):
        ddd_mensuration.innerHTML="""
        <p id="p1">Find↴____</p>
        <div class="oprow7">
         <button id="cube_volume">Volume of cube</button>
         <button id="cube_TSA">TS Area of cube</button>
        </div>
        """

        @when("click", "#cube_volume")
        def make_multidisplay(event):
            global mode, display10, active_display
            mode = "v_cube"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="Enter side of cube.." id="display10" readonly>
            </div>
            """
            display10 = document.querySelector("#display10")
            

            
            active_display = display10
            display10.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display10.addEventListener("click", proxy_fn)
            display10.addEventListener("focus", proxy_fn)


        @when("click", "#cube_TSA")
        def make_multidisplay(event):
            global mode, display10, active_display
            mode = "cube_TSA"
            display.value = "" 
      
            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="Enter side of cube.." id="display10" readonly>
            </div>
            """
            display10 = document.querySelector("#display10")
            
      
            
            active_display = display10
            display10.focus()
      
            
            proxy_fn = create_proxy(set_active_display)
            display10.addEventListener("click", proxy_fn)
            display10.addEventListener("focus", proxy_fn)



        
      @when("click","#cuboid")
      def select_cube(event):
        ddd_mensuration.innerHTML="""
        <p id="p1">Find↴____</p>
        <div class="oprow7">
         <button id="cuboid_volume">Volume of cuboid</button>
         <button id="cuboid_TSA">TS Area of cuboid</button>
        </div>
        """

        @when("click", "#cuboid_volume")
        def make_multidisplay(event):
            global mode, display12, display13, display14 ,active_display
            mode = "cuboid_volume"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="length.." id="display12" readonly>
             <input type="text" placeholder="breadth.." id="display13" readonly>
             <input type="text" placeholder="height.." id="display14" readonly>
            </div>
            """
            display12 = document.querySelector("#display12")
            display13 = document.querySelector("#display13")
            display14 = document.querySelector("#display14")

            
            active_display = display12
            display12.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display12.addEventListener("click", proxy_fn)
            display13.addEventListener("click", proxy_fn)
            display14.addEventListener("click", proxy_fn)
            display12.addEventListener("focus", proxy_fn)
            display13.addEventListener("focus", proxy_fn)
            display14.addEventListener("focus", proxy_fn)

        @when("click", "#cuboid_TSA")
        def make_multidisplay(event):
            global mode, display12, display13, display14 ,active_display
            mode = "cuboid_TSA"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="enter(l*b).." id="display12" readonly>
             <input type="text" placeholder="enter(b*h).." id="display13" readonly>
             <input type="text" placeholder="enter(h*l).." id="display14" readonly>
            </div>
            """
            display12 = document.querySelector("#display12")
            display13 = document.querySelector("#display13")
            display14 = document.querySelector("#display14")

            
            active_display = display12
            display12.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display12.addEventListener("click", proxy_fn)
            display13.addEventListener("click", proxy_fn)
            display14.addEventListener("click", proxy_fn)
            display12.addEventListener("focus", proxy_fn)
            display13.addEventListener("focus", proxy_fn)
            display14.addEventListener("focus", proxy_fn)

      
      @when("click","#cylinder")
      def select_cube(event):
        ddd_mensuration.innerHTML="""
        <p id="p1">Find↴____</p>
        <div class="oprow7">
         <button id="cylinder_volume">Volume of cylinder</button>
         <button id="cylinder_TSA">TS Area of cylinder</button>
        </div>
        <div class="oprow7">
         <button id="cylinder_CSA">CS Area of cylinder</button>
        </div>
        """
        

        @when("click", "#cylinder_volume")
        def make_multidisplay(event):
            global mode,display8,display9, active_display
            mode = "cylinder_volume"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="radius..." id="display8" readonly>
             <input type="text" placeholder="height..." id="display9" readonly>
            </div>
            """
            display8 = document.querySelector("#display8")
            display9 = document.querySelector("#display9")

            
            active_display = display8
            display8.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display8.addEventListener("click", proxy_fn)
            display9.addEventListener("click", proxy_fn)
            display8.addEventListener("focus", proxy_fn)
            display9.addEventListener("focus", proxy_fn)
          
        @when("click", "#cylinder_TSA")
        def make_multidisplay(event):
            global mode,display8,display9, active_display
            mode = "cylinder_TSA"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="radius..." id="display8" readonly>
             <input type="text" placeholder="height..." id="display9" readonly>
            </div>
            """
            display8 = document.querySelector("#display8")
            display9 = document.querySelector("#display9")

            
            active_display = display8
            display8.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display8.addEventListener("click", proxy_fn)
            display9.addEventListener("click", proxy_fn)
            display8.addEventListener("focus", proxy_fn)
            display9.addEventListener("focus", proxy_fn)

        @when("click", "#cylinder_CSA")
        def make_multidisplay(event):
            global mode,display8,display9, active_display
            mode = "cylinder_CSA"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="radius..." id="display8" readonly>
             <input type="text" placeholder="height..." id="display9" readonly>
            </div>
            """
            display8 = document.querySelector("#display8")
            display9 = document.querySelector("#display9")

            
            active_display = display8
            display8.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display8.addEventListener("click", proxy_fn)
            display9.addEventListener("click", proxy_fn)
            display8.addEventListener("focus", proxy_fn)
            display9.addEventListener("focus", proxy_fn)



      @when("click","#sphere")
      def select_cube(event):
        ddd_mensuration.innerHTML="""
        <p id="p1">Find↴____</p>
        <div class="oprow7">
         <button id="sphere_volume">Volume of sphere</button>
         <button id="sphere_SA">surface Area of sphere</button>
        </div>
        """
        @when("click", "#sphere_volume")
        def make_multidisplay(event):
            global mode, display10, active_display
            mode = "sphere_volume"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="Enter radius of sphere.." id="display10" readonly>
            </div>
            """
            display10 = document.querySelector("#display10")
            

            
            active_display = display10
            display10.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display10.addEventListener("click", proxy_fn)
            display10.addEventListener("focus", proxy_fn)


        @when("click", "#sphere_SA")
        def make_multidisplay(event):
            global mode, display10, active_display
            mode = "sphere_SA"
            display.value = "" 
      
            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="Enter radius of sphere.." id="display10" readonly>
            </div>
            """
            display10 = document.querySelector("#display10")
            
      
            
            active_display = display10
            display10.focus()
      
            
            proxy_fn = create_proxy(set_active_display)
            display10.addEventListener("click", proxy_fn)
            display10.addEventListener("focus", proxy_fn)


      @when("click","#cone")
      def select_cube(event):
        ddd_mensuration.innerHTML="""
        <p id="p1">Find↴____</p>
        <div class="oprow7">
         <button id="cone_volume">Volume of cone</button>
         <button id="cone_TSA">TS Area of cone</button>
        </div>
        <div class="oprow7">
         <button id="cone_CSA">CS Area of cone</button>
        </div>
        """

        @when("click", "#cone_volume")
        def make_multidisplay(event):
            global mode,display8,display9, active_display
            mode = "cone_volume"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="radius..." id="display8" readonly>
             <input type="text" placeholder="height..." id="display9" readonly>
            </div>
            """
            display8 = document.querySelector("#display8")
            display9 = document.querySelector("#display9")

            
            active_display = display8
            display8.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display8.addEventListener("click", proxy_fn)
            display9.addEventListener("click", proxy_fn)
            display8.addEventListener("focus", proxy_fn)
            display9.addEventListener("focus", proxy_fn)
          
        @when("click", "#cone_TSA")
        def make_multidisplay(event):
            global mode,display8,display9, active_display
            mode = "cone_TSA"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="radius..." id="display8" readonly>
             <input type="text" placeholder="slant height..." id="display9" readonly>
            </div>
            """
            display8 = document.querySelector("#display8")
            display9 = document.querySelector("#display9")

            
            active_display = display8
            display8.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display8.addEventListener("click", proxy_fn)
            display9.addEventListener("click", proxy_fn)
            display8.addEventListener("focus", proxy_fn)
            display9.addEventListener("focus", proxy_fn)

        @when("click", "#cone_CSA")
        def make_multidisplay(event):
            global mode,display8,display9, active_display
            mode = "cone_CSA"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="radius..." id="display8" readonly>
             <input type="text" placeholder="slant height..." id="display9" readonly>
            </div>
            """
            display8 = document.querySelector("#display8")
            display9 = document.querySelector("#display9")

            
            active_display = display8
            display8.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display8.addEventListener("click", proxy_fn)
            display9.addEventListener("click", proxy_fn)
            display8.addEventListener("focus", proxy_fn)
            display9.addEventListener("focus", proxy_fn)



        
      @when("click","#hemisphere")
      def select_cube(event):
        ddd_mensuration.innerHTML="""
        <p id="p1">Find↴____</p>
        <div class="oprow7">
         <button id="hemisphere_volume">Volume of hemisphere</button>
         <button id="hemisphere_TSA">TS Area of hemispherer</button>
        </div>
        <div class="oprow7">
         <button id="hemisphere_CSA">CS Area of hemisphere</button>
        </div>
        """

        @when("click", "#hemisphere_volume")
        def make_multidisplay(event):
            global mode, display10, active_display
            mode = "hemisphere_volume"
            display.value = "" 

            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="Enter radius of hemisphere.." id="display10" readonly>
            </div>
            """
            display10 = document.querySelector("#display10")
            

            
            active_display = display10
            display10.focus()

            
            proxy_fn = create_proxy(set_active_display)
            display10.addEventListener("click", proxy_fn)
            display10.addEventListener("focus", proxy_fn)


        @when("click", "#hemisphere_TSA")
        def make_multidisplay(event):
            global mode, display10, active_display
            mode = "hemisphere_TSA"
            display.value = "" 
      
            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="Enter radius of hemisphere.." id="display10" readonly>
            </div>
            """
            display10 = document.querySelector("#display10")
            
      
            
            active_display = display10
            display10.focus()
      
            
            proxy_fn = create_proxy(set_active_display)
            display10.addEventListener("click", proxy_fn)
            display10.addEventListener("focus", proxy_fn)

        @when("click", "#hemisphere_CSA")
        def make_multidisplay(event):
            global mode, display10, active_display
            mode = "hemisphere_CSA"
            display.value = "" 
      
            multidisplay.innerHTML = """
            <div class="dualdisplay">
             <input type="text" placeholder="Enter radius of hemisphere.." id="display10" readonly>
            </div>
            """
            display10 = document.querySelector("#display10")
            
      
            
            active_display = display10
            display10.focus()
      
            
            proxy_fn = create_proxy(set_active_display)
            display10.addEventListener("click", proxy_fn)
            display10.addEventListener("focus", proxy_fn)




@when("click", "#result")
def result(event):
    global mode

    
    if mode == "a_rectangle":
        try:
            length = float(display2.value)
            breadth = float(display3.value)
            area = length * breadth
            display.value = int(area) if area.is_integer() else round(area, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid length & breadth"
          
    elif mode == "a_triangle":
        try:
            base = float(display4.value)
            height = float(display5.value)
            area = 1/2*(base * height)
            display.value = int(area) if area.is_integer() else round(area, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid base & height"
          
    elif mode == "a_square":
        try:
            side = float(display6.value)
            area = (side**2)
            display.value = int(area) if area.is_integer() else round(area, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid side of Square"

    elif mode == "a_circle":
        try:
            radius = float(display7.value)
            area = (22/7)*(radius**2)
            display.value = int(area) if area.is_integer() else round(area, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius of circle"

    elif mode == "p_rectangle":
        try:
            length = float(display8.value)
            breadth = float(display9.value)
            perimeter = 2*(length + breadth)
            display.value = int(perimeter) if perimeter.is_integer() else round(perimeter, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid length & breadth"

    elif mode == "p_square":
        try:
            side = float(display10.value)
            perimeter = (side*4)
            display.value = int(perimeter) if perimeter.is_integer() else round(perimeter, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid side of Square"

    elif mode == "p_triangle":
        try:
            side_a = float(display12.value)
            side_b = float(display13.value)
            side_c = float(display14.value)
            perimeter = side_a + side_b + side_c
            display.value = int(perimeter) if perimeter.is_integer() else round(perimeter, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid side's(a,b,c)."

    elif mode == "c_circle":
        try:
            radius = float(display15.value)
            circumference = 2*(22/7)*(radius)
            display.value = int(circumference) if circumference.is_integer() else round(circumference, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius of circle"
          
    elif mode == "v_cube":
        try:
            side = float(display10.value)
            volume = (side**3)
            display.value = int(volume) if volume.is_integer() else round(volume, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid side of cube"
          
    elif mode == "cube_TSA":
        try:
            side = float(display10.value)
            TSA = (6*(side**2))
            display.value = int(TSA) if TSA.is_integer() else round(TSA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid side of cube"

    elif mode == "cuboid_volume":
        try:
            length = float(display12.value)
            breadth = float(display13.value)
            height = float(display14.value)
            volume = length * breadth * height
            display.value = int(volume) if volume.is_integer() else round(volume, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid length, breadth & heigth"

    elif mode == "cuboid_TSA":
        try:
            lb = float(display12.value)
            bh = float(display13.value)
            hl = float(display14.value)
            TSA = 2*(lb + bh + hl)
            display.value = int(TSA) if TSA.is_integer() else round(TSA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid l*b, b*h & h*l"

    elif mode == "cylinder_volume":
        try:
            radius = float(display8.value)
            height = float(display9.value)
            volume = 22/7*(radius**2 * height)
            display.value = int(volume) if volume.is_integer() else round(volume, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius & heigth"
          
    elif mode == "cylinder_CSA":
        try:
            radius = float(display8.value)
            height = float(display9.value)
            TSA = (2*(22/7)*radius * height)
            display.value = int(TSA) if TSA.is_integer() else round(TSA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius & heigth"

    elif mode == "cylinder_TSA":
        try:
            radius = float(display8.value)
            height = float(display9.value)
            CSA = (2*(22/7)*radius * (radius + height))
            display.value = int(CSA) if CSA.is_integer() else round(CSA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius & heigth"

    elif mode == "sphere_volume":
        try:
            radius = float(display10.value)
            volume = 4/3*((22/7)*(radius**3))
            display.value = int(volume) if volume.is_integer() else round(volume, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius"
          
    elif mode == "sphere_SA":
        try:
            radius = float(display10.value)
            SA = 4*(22/7)*(radius**2)
            display.value = int(SA) if SA.is_integer() else round(SA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius"

    elif mode == "cone_volume":
        try:
            radius = float(display8.value)
            height = float(display9.value)
            volume = (1/3)*(22/7)*(radius**2 * height)
            display.value = int(volume) if volume.is_integer() else round(volume, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius & heigth"
          
    elif mode == "cone_CSA":
        try:
            radius = float(display8.value)
            slant_height = float(display9.value)
            CSA = 22/7*radius*slant_height
            display.value = int(CSA) if CSA.is_integer() else round(CSA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius & heigth"

    elif mode == "cone_TSA":
        try:
            radius = float(display8.value)
            slant_height = float(display9.value)
            TSA = ((22/7)*radius * (radius + slant_height))
            display.value = int(TSA) if TSA.is_integer() else round(TSA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid radius & heigth"

    elif mode == "hemisphere_volume":
        try:
            radius = float(display10.value)
            volume = 2/3*22/7*radius**3
            display.value = int(volume) if volume.is_integer() else round(volume, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid side of cube"
          
    elif mode == "hemisphere_TSA":
        try:
            radius = float(display10.value)
            TSA = 3*22/7*radius**2
            display.value = int(TSA) if TSA.is_integer() else round(TSA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid side of cube"

    elif mode == "hemisphere_CSA":
        try:
            radius = float(display10.value)
            CSA = 2*22/7*radius**2
            display.value = int(CSA) if CSA.is_integer() else round(CSA, 4)
        except (ValueError, AttributeError):
            display.value = "Enter valid side of cube"



    elif mode == "xor":
        try:
            logical_xor()
        except (ValueError, SyntaxError):
            display.value = "In-valid expression"
        finally:
            mode = None

    elif mode == "not":
        try:
            logical_not()
        except (ValueError, SyntaxError):
            display.value = "In-valid expression"
        finally:
            mode = None

    elif mode == "xnor":
        try:
            logical_xnor()
        except (ValueError, SyntaxError):
            display.value = "In-valid expression"
        finally:
            mode = None

    elif mode == "bin_dec":
        try:
            bin_to_dec()
        except ValueError:
            display.value = "In-valid Binary"
        finally:
            mode = None

    elif mode == "dec_bin":
        try:
            dec_to_bin()
        except ValueError:
            display.value = "In-valid Decimal"
        finally:
            mode = None

    elif mode == "bin_add":
        try:
            binary_add()
        except ValueError:
            display.value = "In-valid Binary"
        finally:
            mode = None

    elif mode == "bin_sub":
        try:
            binary_subtraction()
        except ValueError:
            display.value = "In-valid Binary"
        finally:
            mode = None

    else:
        try:
            expression = display.value
            answer = eval(expression)
            display.value = int(answer) if answer == int(answer) else round(answer, 5)
        except ZeroDivisionError:
            display.value = "ZeroDivisionError"
        except SyntaxError:
            display.value = "In-valid expression"
        except NameError:
            display.value = "Invalid Input"
        except TypeError:
            display.value = "Type Error"
