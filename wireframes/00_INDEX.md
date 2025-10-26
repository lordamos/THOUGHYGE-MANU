# Thoughtlyfe Website Wireframes - Complete Set

## Overview
This directory contains comprehensive wireframes for the Thoughtlyfe Sacred Geometry website, designed to support Darwin's mission of making sacred geometry accessible for spiritual growth and self-mastery.

## Project Context
- **Platform**: Astro.js with Tailwind CSS
- **Hosting**: Netlify with serverless functions
- **Target Audience**: Spiritual seekers, personal development enthusiasts, sacred geometry practitioners
- **Core Services**: Aura Sync readings, educational courses, book sales

## Wireframes Included

### 1. Homepage (`01_homepage.md`)
**Purpose**: Primary landing page and conversion hub
**Key Features**:
- Video hero section with sacred geometry visuals
- Service previews (Aura Sync, courses, book)
- Darwin introduction and testimonials
- Newsletter signup and clear navigation

**Priority CTAs**:
1. "Book a Reading" (Aura Sync)
2. "Get the Book" (shop redirect)
3. Newsletter subscription

### 2. Aura Sync Readings (`02_aura_sync_readings.md`)
**Purpose**: Primary service booking and conversion page
**Key Features**:
- Three-tier pricing structure (Essential, Complete, Premium)
- Comprehensive booking form with calendar integration
- Service explanation and what clients receive
- Testimonials and FAQ section

**Conversion Flow**:
1. Service explanation builds understanding
2. Pricing comparison facilitates decision
3. Booking form captures leads
4. Follow-up process outlined

### 3. Courses (`03_courses.md`)
**Purpose**: Educational content sales and learning paths
**Key Features**:
- Three structured learning paths (Beginner, Transformation, Mastery)
- Individual course catalog with filtering
- Course detail pages with curriculum
- Student testimonials and learning experience features

**Revenue Model**:
- Bundle packages with savings incentive
- Individual course sales
- Progressive skill development paths

### 4. Shop (`04_shop.md`)
**Purpose**: E-commerce for books, guides, and sacred tools
**Key Features**:
- Featured book prominence (Thoughtlyfe)
- Product categories (Books, Digital Guides, Sacred Tools)
- Shopping cart and secure checkout
- Customer reviews and shipping information

**Product Strategy**:
- Physical and digital book formats
- Supplementary tools and resources
- Bundle opportunities with courses

### 5. About Darwin (`05_about.md`)
**Purpose**: Authority building and trust establishment
**Key Features**:
- Personal story and spiritual journey
- Credentials and teaching philosophy
- Client testimonials and social proof
- Multiple service integration points

**Trust Building Elements**:
- 20+ years experience highlighted
- 1,000+ readings conducted
- Published author credentials
- Clear mission and values

## Design System

### Color Palette (Crystal Design Theme)
- **Primary Purple**: `#3a1c71` - Deep, spiritual, grounding
- **Secondary Teal**: `#00c9a7` - Calming, expansive, insightful  
- **Accent Gold**: `#ffd700` - Enlightenment, prosperity, divine
- **Neutrals**: Light grays and off-whites for balance and readability

### Typography Hierarchy
- **Headings**: Playfair Display (elegant, classic serif)
- **Body Text**: Open Sans (clean, highly readable sans-serif)
- **Sizing**: H1 (48px) → H6 (14px), Body (16px base)

### Responsive Breakpoints
- **Desktop**: 1200px+ (full layouts, multi-column)
- **Tablet**: 768px - 1199px (adapted layouts, two-column)
- **Mobile**: < 768px (single-column, touch-optimized)

## Technical Implementation Notes

### Astro.js Integration
- Static site generation for performance
- Component-based architecture
- Minimal JavaScript, maximum performance
- SEO-optimized out of the box

### Netlify Functions Required
1. **Aura Sync Booking Form**
   - Form validation and processing
   - Email notifications (client + admin)
   - Calendar integration potential
   - Data storage for booking management

2. **Contact Form Processing**
   - Inquiry routing and validation
   - Spam protection
   - Auto-responder setup

3. **Newsletter Subscription**
   - Email service integration (Mailchimp/ConvertKit)
   - Double opt-in workflow
   - List segmentation capabilities

### E-commerce Considerations
- **Initial Phase**: Direct links to Amazon/external retailers
- **Future Phase**: Full e-commerce with payment processing
- **Digital Delivery**: Automated download links post-purchase
- **Inventory Management**: Real-time stock tracking

## User Journey Flows

### Primary User Journey: Aura Sync Booking
1. **Discovery**: Homepage hero or navigation
2. **Education**: Aura Sync page - service explanation
3. **Decision**: Pricing comparison and testimonials
4. **Action**: Booking form completion
5. **Confirmation**: Email confirmation and next steps

### Secondary Journey: Course Enrollment
1. **Discovery**: Homepage preview or direct navigation
2. **Exploration**: Course catalog with filtering
3. **Detail Review**: Individual course pages
4. **Decision**: Learning path vs. individual course
5. **Purchase**: Secure enrollment and payment

### Tertiary Journey: Book Purchase
1. **Introduction**: Homepage or About page mention
2. **Detail**: Shop page or dedicated book section
3. **Decision**: Format selection and reviews
4. **Purchase**: Add to cart and checkout

## Conversion Optimization Strategy

### Trust Building Sequence
1. **Homepage**: Professional presentation and clear value
2. **About Page**: Darwin's credentials and experience
3. **Testimonials**: Social proof throughout site
4. **Guarantees**: Money-back guarantees and secure checkout

### Multiple Touchpoints
- Homepage preview of all services
- Cross-promotion between services
- Email capture for nurturing
- Social media integration for ongoing engagement

## SEO & Content Strategy

### Primary Keywords
- Sacred geometry
- Spiritual readings
- Personal transformation
- Inner peace
- Self-mastery
- Sacred geometry courses

### Content Pillars
1. **Educational**: Sacred geometry principles and applications
2. **Personal**: Transformation stories and testimonials
3. **Practical**: Exercises, meditations, and daily practices
4. **Community**: Student success and connection

## Analytics & Measurement

### Key Metrics to Track
- **Homepage**: Bounce rate, time on page, CTA clicks
- **Aura Sync**: Booking conversion rate, form abandonment
- **Courses**: Enrollment rate, learning path vs. individual
- **Shop**: Add to cart rate, checkout completion
- **About**: Time on page, service page transitions

### Conversion Funnel Analysis
1. Traffic source analysis
2. Page-to-page flow tracking
3. Form completion rates
4. Revenue attribution by source

## Implementation Priority

### Phase 1: Core Pages (MVP)
1. Homepage with video hero
2. Aura Sync booking page
3. About page for authority
4. Basic contact page

### Phase 2: E-commerce & Courses
1. Shop page with book sales
2. Course catalog and detail pages
3. Enhanced booking system
4. Newsletter integration

### Phase 3: Advanced Features
1. User accounts and dashboards
2. Community features
3. Advanced analytics
4. Marketing automation

## Mobile-First Considerations

### Touch Targets
- Minimum 44px for all interactive elements
- Adequate spacing between clickable items
- Thumb-friendly navigation placement

### Performance Optimization
- Lazy loading for images
- Compressed video assets
- Progressive enhancement
- Offline functionality consideration

## Accessibility Standards

### WCAG 2.1 Compliance
- Alt text for all images
- Keyboard navigation support
- Color contrast ratios (AA standard)
- Screen reader compatibility
- Focus indicators for interactive elements

### Inclusive Design
- Simple language and clear instructions
- Multiple ways to access information
- Scalable text and layouts
- Color-blind friendly palette

---

## Next Steps for Development

1. **Design Review**: Validate wireframes against brand guidelines
2. **Content Creation**: Develop actual content for all sections
3. **Asset Gathering**: Collect photos, videos, and graphics
4. **Technical Setup**: Initialize Astro project with components
5. **Backend Development**: Build Netlify functions for forms
6. **Testing Strategy**: Plan for user testing and feedback

This wireframe set provides a complete foundation for building a professional, conversion-optimized website that supports Darwin's mission of sharing sacred geometry wisdom with the world.