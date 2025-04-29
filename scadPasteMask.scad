// Good results printing this with .12 layer, 110% flow, zoffset tight to bed, 
// stepper barely buzzing with no paper 

module bbox() { 
    // a 3D approx. of the children projection on X axis 
    module xProjection() 
        translate([0,1/2,-1/2]) 
            linear_extrude(1) 
                hull() 
                    projection() 
                        rotate([90,0,0]) 
                            linear_extrude(1) 
                                projection() children(); 
  
    // a bounding box with an offset of 1 in all axis
    module bbx()  
        minkowski() { 
            xProjection() children(); // x axis
            rotate(-90)               // y axis
                xProjection() rotate(90) children(); 
            rotate([0,-90,0])         // z axis
                xProjection() rotate([0,90,0]) children(); 
        } 
    
    // offset children() (a cube) by -1 in all axis
    module shrink()
      intersection() {
        translate([ 1, 1, 1]) children();
        translate([-1,-1,-1]) children();
      }

   shrink() bbx() children(); 
}

th = .12 / 25.4;
borderh=1.7/25.4;
borderw=3/25.4; // was 3 
pocket=.3/25.4;
paste_relief=-.02/25.4;

scale([25.4,25.4,25.4])
union() { 
difference() { 
    union() {  
        translate([0,-borderw,0]) 
            translate([-borderw,0,0]) 
                bbox() 
                    linear_extrude(height = borderh, center = false, convexity = 10) 
                        mirror([0,1,0]) 
                            import(str(proj, "-Edge_Cuts.dxf"));
        translate([0,-borderw,0]) 
            translate([+borderw,0,0]) 
                bbox() 
                    linear_extrude(height = borderh, center = false, convexity = 10) 
                        mirror([0,1,0]) 
                            import(str(proj, "-Edge_Cuts.dxf"));
    }
    bbox() linear_extrude(height = borderh, center = false, convexity = 10) 
            mirror([0,1,0]) 
                offset(r=pocket)
			import(str(proj, "-Edge_Cuts.dxf"));
}

difference()  {
    bbox() 
        linear_extrude(height = th, center = false, convexity = 10) 
            mirror([0,1,0]) 
		offset(r=borderw + 5/25.4)
                            import(str(proj, "-Edge_Cuts.dxf"));
        linear_extrude(height = th, center = false, convexity = 10) 
            mirror([0,1,0]) 
                offset(r=paste_relief)
                    import(str(proj, "-F_Paste.dxf"));
 
    
}
}
