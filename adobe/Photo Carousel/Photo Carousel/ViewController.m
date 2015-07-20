//
//  ViewController.m
//  Photo Carousel
//
//  Created by Ravi Vooda on 7/19/15.
//  Copyright (c) 2015 Adobe. All rights reserved.
//

#import "ViewController.h"
#import "UIView+ViewHierarchy.h"

@interface ViewController () <UIScrollViewDelegate> {
    CGFloat width;
    CGFloat padding;
    CGFloat height;
    NSMutableArray *images;
}

@property (strong, nonatomic) NSMutableArray *imageUrls;

@property (strong, nonatomic) UILabel *photoAccessErrorLabel;
@property (strong, nonatomic) ALAssetsLibrary *assetsLibrary;

@property (strong, nonatomic) UIButton *countButton;
@property (strong, nonatomic) UIScrollView *photosScrollView;

@end

@implementation ViewController

const int num_preload = 3;

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    self.photosScrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 30, self.view.frame.size.width, self.view.frame.size.height - 90)];
    [self.photosScrollView setDelegate:self];
    
    // Creating Photo Access Error Label
    self.photoAccessErrorLabel = [[UILabel alloc] initWithFrame:self.view.frame];
    [self.photoAccessErrorLabel setNumberOfLines:0];
    [self.photoAccessErrorLabel setText:@"Sorry! But you have not yet enabled access to photo. \n\nPlease go to ( Settings > Photo Carousel ) to enable access"];
    
    self.countButton = [[UIButton alloc] initWithFrame:CGRectMake(0, 0, 100, 50)];
    [self.countButton setTitle:@"Count" forState:UIControlStateNormal];
    [self.countButton setCenter:CGPointMake(self.view.center.x, (self.view.frame.size.height + CGRectGetMaxY(self.photosScrollView.frame)) / 2)];
    [self.countButton setBackgroundColor:[UIColor blueColor]];
    [self.countButton.layer setCornerRadius:4.0f];
    
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
                    NSURL *image_url = [[result defaultRepresentation] url]; //[[UIImage alloc] initWithCGImage:[result thumbnail]];//[UIImage imageWithCGImage:[[result defaultRepresentation] fullScreenImage]];
                    NSLog(@"Loaded image: %d", (int)index);
                    if (image_url) {
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
    width = self.photosScrollView.frame.size.width - 50;
    
    NSUInteger size = [self.imageUrls count];
    images = [[NSMutableArray alloc] initWithCapacity:size];
    CGSize contentSize = CGSizeMake(size * width + (size + 1) * padding, height);
    [self.photosScrollView setContentSize:contentSize];
    [self.photosScrollView setContentOffset:CGPointMake((size - 1) * width + size * padding, 0) animated:YES];
    
    for (NSUInteger i = 0; i < [self.imageUrls count]; i++) {
        UIImageView *photoImageView = [[UIImageView alloc] initWithFrame:CGRectMake((i+1)*padding + i * width, padding, width, height)];
        [photoImageView setContentMode:UIViewContentModeScaleAspectFit];
        [self.photosScrollView addSubview:photoImageView];
        [images addObject:[NSNull null]];
    }
    NSLog(@"Num photos added: %ld", size);
}

-(void) demandLoadAtIndex:(NSUInteger)index {
    NSLog(@"Loading at index: %ld", index);
    for (NSUInteger i = index; i > MAX(index - num_preload,0); i--) {
        UIImageView *imageView = [self.photosScrollView subviews][i];
        if (!imageView) {
            NSLog(@"No Image View yet");
            return;
        }
        UIImage *loadedImage = images[i];
        if (!loadedImage || [loadedImage isKindOfClass:[NSNull class]]) {
            [self.assetsLibrary assetForURL:self.imageUrls[i] resultBlock:^(ALAsset *asset) {
                NSLog(@"Fetched image at %ld", index);
                UIImage *image = [UIImage imageWithCGImage:[[asset defaultRepresentation] fullScreenImage] scale:1.0f orientation:UIImageOrientationUp];
                [images setObject:image atIndexedSubscript:i];
                [imageView setImage:image];
            } failureBlock:^(NSError *error) {
                NSLog(@"Error occurred in loading image: %ld\n Error: %@",i, [error localizedDescription]);
            }];
        }
    }
}

#pragma mark - Scroll View Delegate Methods
-(void)scrollViewDidScroll:(UIScrollView *)scrollView {
    CGPoint offset = scrollView.contentOffset;
    NSUInteger index = offset.x / (width + padding);
    [self demandLoadAtIndex:index];
}

@end
