import 'package:flutter/material.dart';
import '../theme.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import 'delivery_tracking_screen.dart';

class OrdersScreen extends StatefulWidget {
  const OrdersScreen({super.key});

  @override
  State<OrdersScreen> createState() => _OrdersScreenState();
}

class _OrdersScreenState extends State<OrdersScreen> {
  List<dynamic> _orders = [];
  int _pendingCount = 0;
  int _preparingCount = 0;
  int _completedCount = 0;
  String _filter = 'ALL';
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadOrders();
  }

  Future<void> _loadOrders() async {
    final userId = await AuthService.getUserId();
    if (userId == null) return;

    final res = await ApiService.get('/api/user/$userId/orders');
    if (res != null && res is Map) {
      setState(() {
        _orders = res['orders'] ?? [];
        _pendingCount = res['pending_count'] ?? 0;
        _preparingCount = res['preparing_count'] ?? 0;
        _completedCount = res['completed_count'] ?? 0;
        _loading = false;
      });
    } else {
      setState(() => _loading = false);
    }
  }

  List<dynamic> get _filteredOrders {
    if (_filter == 'ALL') return _orders;
    if (_filter == 'DELIVERY') {
      return _orders.where((o) => o['dining_option'] == 'DELIVERY').toList();
    }
    return _orders.where((o) => o['status'] == _filter).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'My Orders',
          style: AppTextStyles.heading.copyWith(fontSize: 20),
        ),
        centerTitle: true,
      ),
      body: _loading
          ? const Center(
              child: CircularProgressIndicator(color: AppColors.primary),
            )
          : RefreshIndicator(
              color: AppColors.primary,
              onRefresh: _loadOrders,
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    // Stats Cards
                    Row(
                      children: [
                        _statCard(
                          '${_orders.length}',
                          'Total',
                          Icons.receipt,
                          AppColors.primary,
                        ),
                        const SizedBox(width: 8),
                        _statCard(
                          '$_pendingCount',
                          'Pending',
                          Icons.schedule,
                          AppColors.warning,
                        ),
                        const SizedBox(width: 8),
                        _statCard(
                          '$_preparingCount',
                          'Preparing',
                          Icons.restaurant,
                          AppColors.info,
                        ),
                        const SizedBox(width: 8),
                        _statCard(
                          '$_completedCount',
                          'Done',
                          Icons.check_circle,
                          AppColors.success,
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),

                    // Filter tabs
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          _filterChip('All', 'ALL'),
                          _filterChip('Pending', 'PENDING'),
                          _filterChip('Preparing', 'PREPARING'),
                          _filterChip('Delivery', 'DELIVERY'),
                          _filterChip('Completed', 'COMPLETED'),
                          _filterChip('Cancelled', 'CANCELLED'),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Orders list
                    if (_filteredOrders.isEmpty)
                      _emptyState()
                    else
                      ..._filteredOrders.map((o) => _orderCard(o)),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _statCard(String value, String label, IconData icon, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 6),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8),
          ],
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(height: 4),
            Text(
              value,
              style: TextStyle(
                fontWeight: FontWeight.w800,
                fontSize: 18,
                color: AppColors.textMain,
              ),
            ),
            Text(
              label,
              style: TextStyle(color: AppColors.textMuted, fontSize: 10),
            ),
          ],
        ),
      ),
    );
  }

  Widget _filterChip(String label, String value) {
    final selected = _filter == value;
    return GestureDetector(
      onTap: () => setState(() => _filter = value),
      child: Container(
        margin: const EdgeInsets.only(right: 8),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: selected ? AppColors.primary : Colors.white,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: selected
                ? AppColors.primary
                : AppColors.textMuted.withOpacity(0.3),
          ),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: selected ? Colors.white : AppColors.textMain,
            fontWeight: FontWeight.w600,
            fontSize: 13,
          ),
        ),
      ),
    );
  }

  Widget _orderCard(dynamic o) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 10),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Order #${o['id']}',
                style: const TextStyle(
                  fontFamily: 'Georgia',
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                ),
              ),
              _statusBadge(o['status']),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            o['created_at'] ?? '',
            style: AppTextStyles.muted.copyWith(fontSize: 12),
          ),
          const Divider(height: 20),

          // Items
          if (o['items'] != null)
            ...List.generate((o['items'] as List).length, (i) {
              final item = o['items'][i];
              return Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Row(
                  children: [
                    Text(
                      '${item['quantity']}x ',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 13,
                        color: AppColors.primary,
                      ),
                    ),
                    Expanded(
                      child: Text(
                        item['name'] ?? '',
                        style: const TextStyle(fontSize: 13),
                      ),
                    ),
                    Text(
                      '₱${(item['price'] as num).toStringAsFixed(2)}',
                      style: AppTextStyles.muted.copyWith(fontSize: 12),
                    ),
                  ],
                ),
              );
            }),
          const Divider(height: 16),

          // Bottom row
          Row(
            children: [
              if (o['dining_option'] != null)
                _infoBadge(
                  o['dining_option'] == 'DINE_IN'
                      ? 'Dine In'
                      : o['dining_option'] == 'DELIVERY'
                          ? 'Delivery'
                          : 'Take Out',
                  o['dining_option'] == 'DELIVERY'
                      ? Icons.delivery_dining
                      : Icons.restaurant,
                ),
              const SizedBox(width: 6),
              if (o['payment_method'] != null)
                _infoBadge(
                  o['payment_method'] == 'COUNTER' ? 'Counter' : 'GCash',
                  Icons.payment,
                ),
              const Spacer(),
              Text(
                '₱${(o['total_amount'] as num).toStringAsFixed(2)}',
                style: TextStyle(
                  fontFamily: 'Georgia',
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                  color: AppColors.primary,
                ),
              ),
            ],
          ),

          // Track Delivery button for active delivery orders
          if (o['dining_option'] == 'DELIVERY' &&
              o['status'] != 'CANCELLED' &&
              o['status'] != 'COMPLETED') ...[
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => DeliveryTrackingScreen(
                        orderId: o['id'],
                        deliveryAddress: o['delivery_address'],
                      ),
                    ),
                  );
                },
                icon: const Icon(Icons.location_on, size: 18),
                label: const Text('Track Delivery'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                  padding: const EdgeInsets.symmetric(vertical: 10),
                ),
              ),
            ),
          ],

          // Review button for completed orders
          if (o['status'] == 'COMPLETED' && o['review_rating'] == null) ...[
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () => _showReviewDialog(o['id']),
                icon: const Icon(Icons.star_outline, size: 18),
                label: const Text('Leave a Review'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: AppColors.accent,
                  side: BorderSide(color: AppColors.accent.withOpacity(0.5)),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                ),
              ),
            ),
          ],

          if (o['review_rating'] != null) ...[
            const SizedBox(height: 10),
            Row(
              children: [
                ...List.generate(
                  5,
                  (i) => Icon(
                    i < (o['review_rating'] as int)
                        ? Icons.star
                        : Icons.star_border,
                    color: AppColors.gold,
                    size: 18,
                  ),
                ),
                const SizedBox(width: 6),
                Text(
                  'Reviewed',
                  style: TextStyle(
                    color: AppColors.success,
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ],

          if (o['notes'] != null && o['notes'] != '') ...[
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppColors.primary.withOpacity(0.04),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  Icon(Icons.note, color: AppColors.textMuted, size: 14),
                  const SizedBox(width: 6),
                  Expanded(
                    child: Text(
                      o['notes'],
                      style: AppTextStyles.muted.copyWith(fontSize: 12),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _infoBadge(String label, IconData icon) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: AppColors.primary.withOpacity(0.06),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: AppColors.textMuted, size: 12),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              color: AppColors.textMuted,
              fontSize: 10,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _statusBadge(String status) {
    Color bg, fg;
    switch (status) {
      case 'CONFIRMED':
        bg = AppColors.success.withOpacity(0.1);
        fg = AppColors.success;
        break;
      case 'COMPLETED':
        bg = AppColors.success.withOpacity(0.1);
        fg = AppColors.success;
        break;
      case 'PENDING':
        bg = AppColors.warning.withOpacity(0.1);
        fg = AppColors.warning;
        break;
      case 'PREPARING':
        bg = AppColors.info.withOpacity(0.1);
        fg = AppColors.info;
        break;
      case 'CANCELLED':
        bg = AppColors.danger.withOpacity(0.1);
        fg = AppColors.danger;
        break;
      default:
        bg = Colors.grey.withOpacity(0.1);
        fg = Colors.grey;
    }
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        status[0] + status.substring(1).toLowerCase(),
        style: TextStyle(color: fg, fontSize: 11, fontWeight: FontWeight.w700),
      ),
    );
  }

  Widget _emptyState() {
    return Container(
      padding: const EdgeInsets.all(40),
      child: Column(
        children: [
          Icon(
            Icons.shopping_bag_outlined,
            size: 60,
            color: AppColors.primary.withOpacity(0.2),
          ),
          const SizedBox(height: 12),
          Text(
            'No orders found',
            style: AppTextStyles.heading.copyWith(fontSize: 17),
          ),
          const SizedBox(height: 4),
          const Text(
            'Your orders will appear here',
            style: AppTextStyles.muted,
          ),
        ],
      ),
    );
  }

  void _showReviewDialog(int orderId) {
    int rating = 5;
    final commentCtrl = TextEditingController();

    showDialog(
      context: context,
      builder: (ctx) {
        return StatefulBuilder(
          builder: (ctx, setDialogState) {
            return AlertDialog(
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              title: const Text(
                'Rate Your Order',
                style: TextStyle(
                  fontFamily: 'Georgia',
                  fontWeight: FontWeight.bold,
                ),
              ),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(
                      5,
                      (i) => GestureDetector(
                        onTap: () => setDialogState(() => rating = i + 1),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 4),
                          child: Icon(
                            i < rating ? Icons.star : Icons.star_border,
                            color: AppColors.gold,
                            size: 36,
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: commentCtrl,
                    maxLines: 3,
                    decoration: const InputDecoration(
                      hintText: 'Share your experience (optional)',
                    ),
                  ),
                ],
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(ctx),
                  child: const Text('Cancel'),
                ),
                ElevatedButton(
                  onPressed: () async {
                    final userId = await AuthService.getUserId();
                    final res =
                        await ApiService.post('/api/order/$orderId/review', {
                          'user_id': userId,
                          'rating': rating,
                          'comment': commentCtrl.text.trim(),
                        });
                    if (!ctx.mounted) return;
                    Navigator.pop(ctx);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(res['message'] ?? 'Review submitted!'),
                        backgroundColor: res['success'] == true
                            ? AppColors.success
                            : AppColors.danger,
                      ),
                    );
                    _loadOrders();
                  },
                  child: const Text('Submit'),
                ),
              ],
            );
          },
        );
      },
    );
  }
}
