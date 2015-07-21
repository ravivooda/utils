//
//  PCImageView.h
//  Photo Carousel
//
//  Created by Ravi Vooda on 7/20/15.
//  Copyright (c) 2015 Adobe. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface PCImageView : UIImageView

@property (strong, nonatomic) UIImageView *checkImageView;
@property (nonatomic) BOOL isSelected;

-(void)setX:(CGFloat)x;
-(void)setUserTouchedCallBack:(void(^)(BOOL isSelected))callback;

@end
