import 'package:flutter/material.dart';
import '../theme.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';

class ReserveScreen extends StatefulWidget {
  const ReserveScreen({super.key});
  @override
  State<ReserveScreen> createState() => _ReserveScreenState();
}

class _ReserveScreenState extends State<ReserveScreen> {
  DateTime? _date;
  String? _time;
  int _guests = 2;
  final String _bookingType = 'REGULAR';
  final _occasionCtrl = TextEditingController();
  bool _loading = false;
  List<dynamic> _upcoming = [];
  bool _loadingRes = true;
  final List<String> _timeSlots = [];

  @override
  void initState() {
    super.initState();
    for (int h = 11; h <= 20; h++) {
      for (int m = 0; m < 60; m += 30) {
        if (h == 11 && m == 0) continue;
        if (h == 20 && m > 30) continue;
        _timeSlots.add(
          '${h.toString().padLeft(2, '0')}:${m.toString().padLeft(2, '0')}',
        );
      }
    }
    _loadReservations();
  }

  String _fmt(String t) {
    final p = t.split(':');
    int h = int.parse(p[0]);
    final ap = h >= 12 ? 'PM' : 'AM';
    if (h > 12) h -= 12;
    if (h == 0) h = 12;
    return '$h:${p[1]} $ap';
  }

  Future<void> _loadReservations() async {
    final uid = await AuthService.getUserId();
    if (uid == null) return;
    final res = await ApiService.get('/api/user/$uid/reservations');
    if (res != null && res is Map) {
      setState(() {
        _upcoming = res['upcoming'] ?? [];
        _loadingRes = false;
      });
    } else {
      setState(() => _loadingRes = false);
    }
  }

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: now.add(const Duration(days: 1)),
      firstDate: now.add(const Duration(days: 1)),
      lastDate: now.add(const Duration(days: 14)),
      builder: (c, ch) => Theme(
        data: Theme.of(c).copyWith(
          colorScheme: const ColorScheme.light(primary: AppColors.primary),
        ),
        child: ch!,
      ),
    );
    if (picked != null) setState(() => _date = picked);
  }

  Future<void> _submit() async {
    if (_date == null) {
      _msg('Please select a date.', false);
      return;
    }
    if (_time == null) {
      _msg('Please select a time.', false);
      return;
    }
    if (_guests <= 0) {
      _msg('Guest count must be at least 1.', false);
      return;
    }
    if (_guests > 20) {
      _msg('Maximum of 20 guests per reservation.', false);
      return;
    }

    final uid = await AuthService.getUserId();
    if (uid == null) return;
    setState(() => _loading = true);
    final ds =
        '${_date!.year}-${_date!.month.toString().padLeft(2, '0')}-${_date!.day.toString().padLeft(2, '0')}';
    final res = await ApiService.post('/api/reserve', {
      'user_id': uid,
      'date': ds,
      'time': _time,
      'guest_count': _guests,
      'occasion': _occasionCtrl.text.trim(),
      'booking_type': _bookingType,
    });
    setState(() => _loading = false);
    if (res['success'] == true) {
      _msg(res['message'] ?? 'Reservation submitted!', true);
      setState(() {
        _date = null;
        _time = null;
        _guests = 2;
        _occasionCtrl.clear();
      });
      _loadReservations();
    } else {
      _msg(res['message'] ?? 'Failed.', false);
    }
  }

  void _msg(String m, bool ok) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(m),
        backgroundColor: ok ? AppColors.success : AppColors.danger,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Reserve a Table',
          style: AppTextStyles.heading.copyWith(fontSize: 20),
        ),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.04),
                    blurRadius: 12,
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Book Your Visit',
                    style: AppTextStyles.heading.copyWith(fontSize: 18),
                  ),
                  const SizedBox(height: 4),
                  const Text(
                    'Fill in the details below',
                    style: AppTextStyles.muted,
                  ),
                  const SizedBox(height: 20),
                  // Date
                  GestureDetector(
                    onTap: _pickDate,
                    child: Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: AppColors.primary.withOpacity(0.15),
                        ),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Row(
                        children: [
                          const Icon(
                            Icons.calendar_today,
                            color: AppColors.primary,
                            size: 20,
                          ),
                          const SizedBox(width: 12),
                          Text(
                            _date != null
                                ? '${_date!.month}/${_date!.day}/${_date!.year}'
                                : 'Select Date',
                            style: TextStyle(
                              color: _date != null
                                  ? AppColors.textMain
                                  : AppColors.textMuted,
                              fontSize: 15,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 14),
                  // Time
                  DropdownButtonFormField<String>(
                    value: _time,
                    hint: const Text('Select Time'),
                    decoration: const InputDecoration(
                      prefixIcon: Icon(
                        Icons.access_time,
                        color: AppColors.primary,
                      ),
                    ),
                    items: _timeSlots
                        .map(
                          (t) =>
                              DropdownMenuItem(value: t, child: Text(_fmt(t))),
                        )
                        .toList(),
                    onChanged: (v) => setState(() => _time = v),
                  ),
                  const SizedBox(height: 14),
                  // Guests
                  Row(
                    children: [
                      const Icon(
                        Icons.people,
                        color: AppColors.primary,
                        size: 20,
                      ),
                      const SizedBox(width: 12),
                      const Text('Guests: ', style: TextStyle(fontSize: 15)),
                      const Spacer(),
                      Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(25),
                          border: Border.all(
                            color: AppColors.primary.withOpacity(0.2),
                          ),
                        ),
                        child: Row(
                          children: [
                            IconButton(
                              icon: const Icon(Icons.remove, size: 18),
                              onPressed: _guests > 1
                                  ? () => setState(() => _guests--)
                                  : null,
                              color: AppColors.primary,
                              constraints: const BoxConstraints(
                                minWidth: 36,
                                minHeight: 36,
                              ),
                            ),
                            Padding(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 12,
                              ),
                              child: Text(
                                '$_guests',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 18,
                                ),
                              ),
                            ),
                            IconButton(
                              icon: const Icon(Icons.add, size: 18),
                              onPressed: () => setState(() => _guests++),
                              color: AppColors.primary,
                              constraints: const BoxConstraints(
                                minWidth: 36,
                                minHeight: 36,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),
                  // Occasion (Optional)
                  TextField(
                    controller: _occasionCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Occasion (optional)',
                      prefixIcon: Icon(
                        Icons.celebration,
                        color: AppColors.primary,
                      ),
                      hintText: 'Birthday, Anniversary, etc.',
                    ),
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    height: 52,
                    child: ElevatedButton.icon(
                      onPressed: _loading ? null : _submit,
                      icon: _loading
                          ? const SizedBox.shrink()
                          : const Icon(Icons.send),
                      label: _loading
                          ? const SizedBox(
                              width: 22,
                              height: 22,
                              child: CircularProgressIndicator(
                                color: Colors.white,
                                strokeWidth: 2.5,
                              ),
                            )
                          : const Text('Submit Reservation'),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            Text(
              'Upcoming Reservations',
              style: AppTextStyles.heading.copyWith(fontSize: 17),
            ),
            const SizedBox(height: 12),
            if (_loadingRes)
              const Center(
                child: CircularProgressIndicator(color: AppColors.primary),
              )
            else if (_upcoming.isEmpty)
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(14),
                ),
                child: const Column(
                  children: [
                    Icon(
                      Icons.calendar_today,
                      color: AppColors.primary,
                      size: 30,
                    ),
                    SizedBox(height: 8),
                    Text(
                      'No upcoming reservations',
                      style: AppTextStyles.muted,
                    ),
                  ],
                ),
              )
            else
              ..._upcoming.map(
                (r) => Container(
                  margin: const EdgeInsets.only(bottom: 10),
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.04),
                        blurRadius: 8,
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: AppColors.primary.withOpacity(0.08),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: const Icon(
                          Icons.calendar_today,
                          color: AppColors.primary,
                          size: 20,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '${r['date_formatted']} · ${r['time_formatted']}',
                              style: const TextStyle(
                                fontWeight: FontWeight.w700,
                                fontSize: 13,
                              ),
                            ),
                            Text(
                              '${r['guest_count']} guests${r['occasion'] != null && r['occasion'] != '' ? ' · ${r['occasion']}' : ''}',
                              style: AppTextStyles.muted.copyWith(fontSize: 12),
                            ),
                          ],
                        ),
                      ),
                      _badge(r['status']),
                    ],
                  ),
                ),
              ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }

  Widget _badge(String s) {
    final c = s == 'CONFIRMED'
        ? AppColors.success
        : s == 'PENDING'
        ? AppColors.warning
        : Colors.grey;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: c.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        s[0] + s.substring(1).toLowerCase(),
        style: TextStyle(color: c, fontSize: 11, fontWeight: FontWeight.w600),
      ),
    );
  }
}
