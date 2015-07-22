//
//  ViewController.m
//  Photo Carousel
//
//  Created by Ravi Vooda on 7/19/15.
//  Copyright (c) 2015 Adobe. All rights reserved.
//

#import "ViewController.h"
#import "UIView+ViewHierarchy.h"
#import "PCImageView.h"
#import "PCURL.h"

@interface ViewController () <UIScrollViewDelegate> {
    CGFloat padding;
    CGFloat height;
    NSMutableArray *images;
}

@property (strong, nonatomic) NSMutableArray *imageUrls;

@property (strong, nonatomic) UILabel *photoAccessErrorLabel;
@property (strong, nonatomic) ALAssetsLibrary *assetsLibrary;

@property (strong, nonatomic) UIButton *countButton;
@property (strong, nonatomic) UIScrollView *photosScrollView;

@property (nonatomic) int num_selected;

@property (strong, nonatomic) NSDictionary *widthMap;

@end

@implementation ViewController

const int num_preload = 3;

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    self.num_selected = 0;
    
    self.photosScrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 30, self.view.frame.size.width, self.view.frame.size.height - 200)];
    [self.photosScrollView setDelegate:self];
    
    // Creating Photo Access Error Label
    self.photoAccessErrorLabel = [[UILabel alloc] initWithFrame:self.view.frame];
    [self.photoAccessErrorLabel setNumberOfLines:0];
    [self.photoAccessErrorLabel setText:@"Sorry! But you have not yet enabled access to photo. \n\nPlease go to ( Settings > Photo Carousel ) to enable access"];
    [self.photoAccessErrorLabel setTextAlignment:NSTextAlignmentCenter];
    
    self.countButton = [[UIButton alloc] initWithFrame:CGRectMake(0, 0, 100, 50)];
    [self.countButton setTitle:@"Count" forState:UIControlStateNormal];
    [self.countButton setCenter:CGPointMake(self.view.center.x, (self.view.frame.size.height + CGRectGetMaxY(self.photosScrollView.frame)) / 2)];
    [self.countButton setBackgroundColor:[UIColor blueColor]];
    [self.countButton.layer setCornerRadius:4.0f];
    [self.countButton addTarget:self action:@selector(countTapped:) forControlEvents:UIControlEventTouchUpInside];
    
    [self.view addSubview:self.photosScrollView];
    [self.view addSubview:self.photoAccessErrorLabel];
    [self.view addSubview:self.countButton];
}

-(void)viewDidAppear:(BOOL)animated {
    [super viewDidAppear:animated];
    if (!self.assetsLibrary) {
        // We should try to load library
        [self loadLibrary];
    }
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(void)clearDisplay {
    self.imageUrls = [[NSMutableArray alloc] init];
    [self.photosScrollView removeAllSubviews];
    [self.photosScrollView setContentSize:CGSizeZero];
    [self.photosScrollView setContentOffset:CGPointZero];
}

-(void)loadLibrary {
    self.assetsLibrary = [[ALAssetsLibrary alloc] init];
    NSUInteger groupType = ALAssetsGroupAll;
    __weak ViewController *weakSelf = self;
    [self clearDisplay];
    [self.assetsLibrary enumerateGroupsWithTypes:groupType usingBlock:^(ALAssetsGroup *group, BOOL *stop) {
        if (group && group.numberOfAssets > 0) {
            [group enumerateAssetsUsingBlock:^(ALAsset *result, NSUInteger index, BOOL *stop) {
                if (result) {
                    ALAssetRepresentation* representation = [result defaultRepresentation];
                    if (representation) {
                        PCURL *image_url = [[PCURL alloc] initWithString:representation.url.absoluteString];
                        [image_url setSize:representation.dimensions];
                        [weakSelf.imageUrls addObject:image_url];
                    }
                }
            }];
        } else if (!group) {
            // So we reached the end of the photos enumeration
            [weakSelf loadImages];
        }
    } failureBlock:^(NSError *error) {
        weakSelf.assetsLibrary = nil;
        [weakSelf.photoAccessErrorLabel setHidden:NO];
        [weakSelf.countButton setHidden:YES];
    }];
}

-(void)loadImages {
    [self.photoAccessErrorLabel setHidden:YES];
    [self.countButton setHidden:NO];
    
    padding = 10;
    height = self.photosScrollView.frame.size.height;
    
    NSUInteger size = [self.imageUrls count];
    images = [[NSMutableArray alloc] initWithCapacity:size];
    self.widthMap = [[NSMutableDictionary alloc] initWithCapacity:size];
    
    CGFloat width_scroll = 0;
    
    __weak ViewController *weakSelf = self;
    
    for (NSUInteger i = 0; i < [self.imageUrls count]; i++) {
        PCURL *url = self.imageUrls[i];
        CGFloat width_image = url.size.width * height / url.size.height;
        PCImageView *photoImageView = [[PCImageView alloc] initWithFrame:CGRectMake(padding + width_scroll, padding, width_image, height)];
        UILabel * countLabel = [[UILabel alloc] initWithFrame:photoImageView.bounds];
        [countLabel setTextAlignment:NSTextAlignmentCenter];
        [countLabel setText:[NSString stringWithFormat:@"%d",(int)i]];
        [photoImageView addSubview:countLabel];
        width_scroll += width_image + padding;
        [photoImageView setContentMode:UIViewContentModeScaleAspectFill];
        [photoImageView setClipsToBounds:YES];
        [self.photosScrollView addSubview:photoImageView];
        [images addObject:[NSNull null]];
        [photoImageView setUserTouchedCallBack:^(BOOL isSelected) {
            if (isSelected) {
                weakSelf.num_selected++;
            } else {
                weakSelf.num_selected--;
            }
        }];
    }
    
    if ([self.imageUrls count] > 0) {
        width_scroll += padding;
    }
    
    [self.photosScrollView setContentSize:CGSizeMake(width_scroll, self.photosScrollView.frame.size.height)];
    //[self.photosScrollView setContentOffset:CGPointMake((size - 1) * width + size * padding, 0) animated:YES];
    NSLog(@"Num photos added: %ld", size);
}

-(void) demandLoadAtIndex:(NSUInteger)index {
    NSLog(@"Loading at index: %ld", index);
    for (NSUInteger i = index; i >= MAX((int)index - num_preload,0) && i < [self.imageUrls count]; i--) {
        UIImageView *imageView = [self.photosScrollView subviews][i];
        if (!imageView) {
            NSLog(@"No Image View yet");
            return;
        }
        UIImage *loadedImage = images[i];
        if (!loadedImage || [loadedImage isKindOfClass:[NSNull class]]) {
            [self.assetsLibrary assetForURL:self.imageUrls[i] resultBlock:^(ALAsset *asset) {
                NSLog(@"Fetched image at %ld", i);
                UIImage *image = [UIImage imageWithCGImage:[[asset defaultRepresentation] fullScreenImage] scale:1.0f orientation:UIImageOrientationUp];
                [images setObject:image atIndexedSubscript:i];
                [imageView setImage:image];
            } failureBlock:^(NSError *error) {
                NSLog(@"Error occurred in loading image: %ld\n Error: %@",i, [error localizedDescription]);
            }];
        }
    }
}

-(void)countTapped:(UIButton*)sender {
    UIAlertView *alertSelectedCount = [[UIAlertView alloc] initWithTitle:@"Selected images count" message:[NSString stringWithFormat:@"%d",self.num_selected] delegate:nil cancelButtonTitle:@"Okay" otherButtonTitles:nil];
    [alertSelectedCount show];
}

#pragma mark - Scroll View Delegate Methods
-(void)scrollViewDidScroll:(UIScrollView *)scrollView {
    CGPoint offset = scrollView.contentOffset;
    NSUInteger index = offset.x / (width + padding);
    [self demandLoadAtIndex:index];
    
    // Set Frame for checkmark at i - 1
    if ((int)index - 1 > 0) {
        PCImageView *imageView = [self.photosScrollView subviews][index-1];
        CGRect relativeRect = [self.view convertRect:imageView.frame fromView:self.photosScrollView];
        [imageView setX:self.view.frame.size.width - relativeRect.origin.x];
    }
    
    // Set Frame for checkmark at i
    PCImageView *imageView = [self.photosScrollView subviews][index];
    CGRect relativeRect = [self.view convertRect:imageView.frame fromView:self.photosScrollView];
    [imageView setX:self.view.frame.size.width - relativeRect.origin.x];
    
    // Set Frame for checkmark at i + 1
    if ((int)index + 1 < [self.imageUrls count]) {
        PCImageView *imageView = [self.photosScrollView subviews][index+1];
        CGRect relativeRect = [self.view convertRect:imageView.frame fromView:self.photosScrollView];
        [imageView setX:self.view.frame.size.width - relativeRect.origin.x];
    }
}

@end
