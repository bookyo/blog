# 8 Beautiful shadcn/ui Components That Will Transform Your React Apps

shadcn/ui isn't a component library you install. It's a collection of components you copy, own, and customize directly into your project. No black-box package updates. No fighting framework versions. Just clean, accessible, production-ready React components built on Radix UI and styled with Tailwind CSS.

Here's 8 shadcn/ui components that will genuinely change how you build React interfaces.

## 1. Button — The Foundation of Every UI

Every UI starts with a button, and shadcn/ui's Button component is the gold standard. It ships with 7 visual variants (default, destructive, outline, secondary, ghost, link, and a loading state) plus 3 size options.

```tsx
<Button variant="destructive">Delete Account</Button>
<Button size="lg">Get Started</Button>
<Button loading>Processing...</Button>
```

What makes it special isn't the variants — it's that `loading` state. Pass it and the button automatically shows a spinner while staying the same size. No layout shift. No custom logic.

This means you can wrap any async action without touching the button's styling.

## 2. Card — Your Dashboard's Best Friend

Cards are the building blocks of data-heavy interfaces, and shadcn/ui's Card system is thoughtfully split into four parts: Header, Title, Description, Content, and Footer. Each can be used independently or composed together.

The result is cards that look polished without any custom CSS:

```tsx
<Card>
  <CardHeader>
    <CardTitle>$45,231</CardTitle>
    <CardDescription>Total Revenue</CardDescription>
  </CardHeader>
  <CardContent>
    <Badge className="bg-green-100 text-green-800">+20.1%</Badge>
  </CardContent>
</Card>
```

In other words, your dashboard metrics card is now 6 lines of readable JSX instead of a CSS battleground.

## 3. Data Table — The Component Everyone Rewrites

Building data tables from scratch is a rite of passage every React developer goes through. The shadcn/ui Table component gives you a clean, accessible table implementation that handles sorting, pagination, and row actions without locking you into a specific data framework.

```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
      <TableHead className="text-right">Actions</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {users.map((user) => (
      <TableRow key={user.id}>
        <TableCell>{user.name}</TableCell>
        <TableCell><Badge>Active</Badge></TableCell>
        <TableCell className="text-right">
          <DropdownMenu>...</DropdownMenu>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

This means you get a real table — with proper `role="grid"` semantics — in about 20 lines of JSX. The action menu tied to each row is a DropdownMenu component, so it slots in perfectly.

## 4. Dialog — Modal Windows That Don't Fight You

Dialog (the shadcn/ui name for modals) uses Radix UI's dialog primitive, which means it handles focus trapping, scroll locking, and keyboard navigation correctly out of the box.

```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button variant="destructive">Delete Item</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Are you sure?</DialogTitle>
      <DialogDescription>
        This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button variant="destructive">Delete</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

The `asChild` prop on DialogTrigger is a pattern you'll see across shadcn/ui: it lets you use any element as the trigger while keeping all the accessibility behavior. This means a `<button>` opens the dialog, but so does a `<div>` or an `<Avatar>`, and screen readers understand all of them.

## 5. Command Palette — The GitHub-Style Search Every App Needs

Command palettes (⌘K to open) have become a standard UX pattern since GitHub introduced theirs. shadcn/ui ships a full implementation via the Command component, complete with search, grouped results, and keyboard navigation.

```tsx
<CommandDialog open={open} onOpenChange={setOpen}>
  <CommandInput placeholder="Type a command or search..." />
  <CommandList>
    <CommandEmpty>No results found.</CommandEmpty>
    <CommandGroup heading="Suggestions">
      <CommandItem>📅 Calendar</CommandItem>
      <CommandItem>🔍 Search</CommandItem>
      <CommandItem>⚙️ Settings</CommandItem>
    </CommandGroup>
  </CommandList>
</CommandDialog>
```

This means adding a GitHub-style command palette to your app takes about 15 lines. In other words, this is a feature you'd ship to production in an afternoon.

## 6. Tabs — Clean Content Switching

Tabs are deceptively complex to build correctly. The shadcn/ui Tabs component handles keyboard navigation (arrow keys to switch tabs), proper ARIA roles, and focus management without you writing a single line of accessibility code.

```tsx
<Tabs defaultValue="account" className="w-full max-w-md">
  <TabsList className="grid w-full grid-cols-3">
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="password">Password</TabsTrigger>
    <TabsTrigger value="notifications">Notifications</TabsTrigger>
  </TabsList>
  <TabsContent value="account">...</TabsContent>
  <TabsContent value="password">...</TabsContent>
  <TabsContent value="notifications">...</TabsContent>
</Tabs>
```

The `grid-cols-3` class makes the tabs look like a segmented control — a native iOS pattern. This means you get platform-native feel without any platform-specific code.

## 7. Sheet — Slide-Over Panels Without the Pain

Sheets (slide-over panels, also called drawers) are the mobile-friendly alternative to dialogs when you need to show supplementary content without interrupting the user's flow. The shadcn/ui Sheet component uses the same Radix primitive pattern as Dialog, so all the accessibility is handled.

```tsx
<Sheet>
  <SheetTrigger asChild>
    <Button>Edit Profile</Button>
  </SheetTrigger>
  <SheetContent>
    <SheetHeader>
      <SheetTitle>Edit Profile</SheetTitle>
      <SheetDescription>
        Make changes and click save when done.
      </SheetDescription>
    </SheetHeader>
    <div className="grid gap-4 py-4">
      <Input placeholder="Your name" />
      <Input placeholder="Your email" />
    </div>
    <SheetFooter>
      <Button type="submit">Save changes</Button>
    </SheetFooter>
  </SheetContent>
</Sheet>
```

On mobile, this slides in from the right edge. On desktop, it appears as a narrower side panel. The same component adapts to both. This means you ship one component and get responsive behavior for free.

## 8. Avatar — User Identity at a Glance

Avatars seem trivial until you need to handle missing images, long names, and multiple sizes across your app. shadcn/ui's Avatar component handles all three:

```tsx
<Avatar className="h-12 w-12">
  <AvatarImage src="/user-photo.jpg" alt="@user" />
  <AvatarFallback>JD</AvatarFallback>
</Avatar>
```

The `<AvatarFallback>` shows initials when the image fails to load — and it waits until that happens, so you never see a broken image icon. For apps with user-generated photos, this is the difference between an interface that feels polished and one that looks broken.

## The shadcn/ui Difference

Most component libraries give you a black box. shadcn/ui gives you the source code.

Every component is a file in your project. When your designer asks for a subtle change, you open the component and adjust it. When a bug appears, you fix it. When your team needs a custom variant, you extend what's already there.

This means shadcn/ui components don't fight your design system — they become part of it.

Explore the full component library and copy what you need at [shadcn/ui on ElysiaTools](https://elysiatools.com/en/samples/shadcn-ui). All examples are free, run in your browser, and come with copy-paste ready code.
