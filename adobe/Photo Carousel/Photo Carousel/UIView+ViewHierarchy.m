//
//  UIView+ViewHierarchy.m
//  Photo Carousel
//
//  Created by Ravi Vooda on 7/19/15.
//  Copyright (c) 2015 Adobe. All rights reserved.
//

#import "UIView+ViewHierarchy.h"

@implementation UIView (ViewHierarchy)

-(void)removeAllSubviews {
    for (UIView *subview in [self subviews]) {
        [subview removeFromSuperview];
    }
}

@end
