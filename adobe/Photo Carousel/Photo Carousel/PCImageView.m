//
//  PCImageView.m
//  Photo Carousel
//
//  Created by Ravi Vooda on 7/20/15.
//  Copyright (c) 2015 Adobe. All rights reserved.
//

#import "PCImageView.h"

@interface PCImageView ()

@property (nonatomic, copy) void (^completion)(BOOL isSelected);
@property (strong, nonatomic) UIImageView *checkImageView;

@end

@implementation PCImageView

const int padding = 5;

-(instancetype)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
        self.checkImageView = [[UIImageView alloc] initWithImage:[UIImage imageNamed:@"checkmark"]];
        [self setFrame:frame];
        [self addSubview:self.checkImageView];
        [self setUserInteractionEnabled:YES];
        UITapGestureRecognizer *tapGesture = [[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(tapCallBack:)];
        [self addGestureRecognizer:tapGesture];
        [self setIsSelected:NO];
    }
    return self;
}

-(void)setFrame:(CGRect)frame {
    [super setFrame:frame];
    [self.checkImageView setCenter:CGPointMake(frame.size.width - (self.checkImageView.frame.size.width)/2 - padding, frame.size.height - self.checkImageView.frame.size.height)];
}

-(void)setIsSelected:(BOOL)isSelected {
    _isSelected = isSelected;
    if (isSelected) {
        [self.checkImageView setHidden:NO];
    } else {
        [self.checkImageView setHidden:YES];
    }
}

-(void)setUserTouchedCallBack:(void (^)(BOOL))callback {
    self.completion = callback;
}

-(void)tapCallBack:(UITapGestureRecognizer*)recognizer {
    if (self.completion) {
        [self setIsSelected:!self.isSelected];
        self.completion(self.isSelected);
    }
}

@end
